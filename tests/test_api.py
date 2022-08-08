from biofid.tests.base import NoDatabaseTestCase
from biofid.api.responses import modify_header_by_request_suffix


class TestApi(NoDatabaseTestCase):
    def test_suffix_response_with_json(self):
        header = {'HTTP_ACCEPT': 'application/html'}
        test_urls = ['/path/to/uri.json', '/path/to/uri.html', '/path/to/uri.rdf', '/path/to/.jsonuri',
                     '/path/to/uri.path']
        expected_headers = ['application/json', 'application/html', 'application/rdf+xml', 'application/html',
                            'application/html']

        for test_url, expected_header in zip(test_urls, expected_headers):
            with self.subTest(msg=f'URL "{test_url}"'):
                request = self.request_factory.get(test_url, **header)
                self.assertEqual(request.META['HTTP_ACCEPT'], 'application/html')

                modify_header_by_request_suffix(request)

                self.assertEqual(request.META['HTTP_ACCEPT'], expected_header)
