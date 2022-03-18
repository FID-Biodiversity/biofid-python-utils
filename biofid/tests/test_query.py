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
            ('echo $SECRET', 'echo \$SECRET')
        ]

        for solr_input, expected_result in test_cases:
            with self.subTest(solr_input):
                self.assertEquals(expected_result, query.escape_solr_input(solr_input))
