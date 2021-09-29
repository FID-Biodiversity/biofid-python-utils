from biofid.tests.base import NoDatabaseTestCase
from biofid.data import url as url_module


class TestUrl(NoDatabaseTestCase):
    def test_is_url(self):
        testcases = [
            ('https://www.biofid.de', True),
            ('https://www.biofid.de/', True),
            ('https://www.biofid.de/search/', True),
            ('http://biofid.de', True),
            ('http:www.biofid.de', False),
            ('http://localhost/', True),
            ('http://localhost:8000/foo', True),
            ('test', False),
            ('some test referencing https://www.biofid.de.', False),
            ('some%20test%20with%20encoding%20and%20referencing%20https://www.biofid.de.', False),
            ('https://www.biofid.de%20and%20more', False),
            ('www.biofid.de', True),
            ('www.this-is-valid.com', True),
            ('www.com', False)
        ]

        for url, expectation in testcases:
            with self.subTest(url):
                self.assertEquals(url_module.is_url(url), expectation)
