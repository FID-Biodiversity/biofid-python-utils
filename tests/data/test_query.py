from biofid.tests.base import NoDatabaseTestCase
from biofid.data import query


class TestQuery(NoDatabaseTestCase):
    def test_solr_escaping(self):
        test_cases = [
            ('foo bar', 'foo bar'),
            ('foo || bar', 'foo \|\| bar'),
            ('foo ? bar', 'foo \? bar'),
            ('(1+1):2', '\(1\+1\)\:2'),
            ('"foo bar"', '"foo bar"'),
            ("'foo bar'", "'foo bar'"),
            ('echo $SECRET', 'echo \$SECRET'),
            (-1, -1)
        ]

        for solr_input, expected_result in test_cases:
            with self.subTest(solr_input):
                self.assertEqual(expected_result, query.escape_solr_input(solr_input))

    def test_escape_sparql_string(self):
        test_cases = [
            ('https://www.biofid.de/bio-ontologies/Tracheophyta/gbif/12345',
             'https://www.biofid.de/bio-ontologies/Tracheophyta/gbif/12345'),
            ('http://www.wikidata.org/entity/Q12345', 'http://www.wikidata.org/entity/Q12345'),
            ('Some arbitrary code including \' and ", but also \\. """',
             'Some arbitrary code including \\\' and \\", but also \\\\. \\"\\"\\"')
        ]

        for string, escaped_string in test_cases:
            with self.subTest(string):
                self.assertEqual(query.escape_sparql_string(string), escaped_string)
