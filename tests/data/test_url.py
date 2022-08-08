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
            ('www.com', False),
            ('https://sws.geonames.org/765280', True),
            ('https://www.biofid.de/bio-ontologies/Tracheophyta/gbif/4928315.html', True),
            ('https://www.wikidata.org/entity/Q1794', True),
            ('https://www.biofid.de/bio-ontologies/tracheophyta#GBIF_3119995', True),
            (('https://www.wikidata.org/entity/Q1794',), False),
            ('https://subsubdomain.subdomain.domain.com/foo', True)
        ]

        for url, expectation in testcases:
            with self.subTest(url):
                self.assertEqual(url_module.is_url(url), expectation)
