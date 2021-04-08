from time import sleep

from django.test import LiveServerTestCase
from django.test import SimpleTestCase
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from django.test import RequestFactory


class NoDatabaseTestCase(SimpleTestCase):
    """ A test class that disables any databases involved and hence runs faster. """
    databases = []

    def setUp(self) -> None:
        self.request_factory = RequestFactory()


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