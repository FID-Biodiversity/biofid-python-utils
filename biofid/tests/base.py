from contextlib import contextmanager
from django.core.handlers.wsgi import WSGIRequest
from django.test import LiveServerTestCase
from django.test import RequestFactory
from django.test import SimpleTestCase
from selenium import webdriver
from time import sleep
from typing import Any
from webdriver_manager.chrome import ChromeDriverManager

AJAX_REQUEST_HEADER = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}


class AjaxRequestFactory(RequestFactory):
    def get(self, path: Any, data: Any = None, secure: bool = False, **extra: Any) -> WSGIRequest:
        extra.update(AJAX_REQUEST_HEADER)
        return super().get(path=path, data=data, secure=secure, **extra)


class NoDatabaseTestCase(SimpleTestCase):
    """ A test class that disables any databases involved and hence runs faster.
        Removes the Diff size of some functions by setting maxDiff = None;
        For details: https://docs.python.org/3/library/unittest.html#unittest.TestCase.maxDiff
    """
    databases = []  # No databases are loaded => Faster
    maxDiff = None

    def __init__(self, methodName: str = 'runTest'):
        super().__init__(methodName)

        self.request_factory = RequestFactory()
        self.ajax_request_factory = AjaxRequestFactory()


class BiofidLiveWebsiteTestCase(LiveServerTestCase):
    """ A test class that comes preconfigured with Selenium. """

    selenium = None
    host = 'localhost'
    port = 8000

    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.headless = True
        chrome_path = ChromeDriverManager().install()

        cls.selenium = webdriver.Chrome(executable_path=chrome_path, chrome_options=options)
        cls.selenium.implicitly_wait(10)

        super(BiofidLiveWebsiteTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(BiofidLiveWebsiteTestCase, cls).tearDownClass()

    def create_test_url(self, sub_page_url: str) -> str:
        """ This method appends the base URL to the given URL path. """
        if not sub_page_url.startswith('/'):
            sub_page_url = '/{}'.format(sub_page_url)

        return '{base_url}{sub_page}'.format(base_url=self.live_server_url, sub_page=sub_page_url)

    def wait(self, waiting_time_in_seconds: int):
        sleep(waiting_time_in_seconds)


@contextmanager
def not_raises(exception):
    """ Makes the intention clear that a function is run for the purpose of not raising a given exception.
        Usage:
            with not_raises(IndexException):
                function_that_should_not_raise()
    """
    try:
        yield
    except exception:
        raise ValueError("DID RAISE {0}".format(exception))
