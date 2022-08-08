from biofid.tests.base import NoDatabaseTestCase
from biofid.data.transformation import graph_data_transformations

data = [
    {'value': '1234', 'datatype': 'http://www.w3.org/2001/XMLSchema#string', 'type': 'typed-literal'},
    {'value': 'Test', 'datatype': 'http://www.w3.org/2001/XMLSchema#string', 'type': 'literal'},
    {'value': '1', 'datatype': 'http://www.w3.org/2001/XMLSchema#boolean', 'type': 'typed-literal'},
    {'value': '0', 'datatype': 'http://www.w3.org/2001/XMLSchema#boolean', 'type': 'typed-literal'},
    {'value': 'https://dwc.tdwg.org/terms/#family', 'datatype': 'uri'},
    {"value": "Rot-Buche", "type": "literal", "xml:lang": "de"},
]

graph_data = [
    {'objectLabel': {'value': '1234', 'datatype': 'http://www.w3.org/2001/XMLSchema#string', 'type': 'typed-literal'}},
    {'predicateLabel': {'value': 'Test', 'datatype': 'http://www.w3.org/2001/XMLSchema#string', 'type': 'literal'}},
    {'object': {'value': '1', 'datatype': 'http://www.w3.org/2001/XMLSchema#boolean', 'type': 'typed-literal'}},
    {'predicate': {'value': '0', 'datatype': 'http://www.w3.org/2001/XMLSchema#boolean', 'type': 'typed-literal'}},
    {'object': {'value': 'https://dwc.tdwg.org/terms/#family', 'datatype': 'uri'}},
    {'objectLabel': {"value": "Rot-Buche", "type": "literal", "xml:lang": "de"}}
]


create_objects_test_data = {'predicate': {'type': 'uri', 'value': 'https://www.biofid.de/bio-ontologies#has_petal_color'},
                            'object': {'type': 'uri', 'value': 'http://purl.obolibrary.org/obo/PATO_0000952'},
                            'predicateLabel': {'type': 'literal', 'value': 'flower color', 'xml:lang': 'en'},
                            'objectLabel': {'type': 'literal', 'value': 'brown'},
                            'subject': {'type': 'uri', 'value': 'http://purl.obolibrary.org/obo/bla'} 
                            }


def run_subtests(test_class, input, expected, func):
    for input, expected_output in zip(input, expected):
        with test_class.subTest(msg=f"Input: {input}; Expected: {expected_output}"):
            test_class.assertEqual(func(input), expected_output)


def assert_object_correct(test_class, created_object, object_type, expected_label, expected_language, expected_uri):
    test_class.assertTrue(isinstance(created_object, object_type))
    test_class.assertEqual(created_object.uri, expected_uri)
    test_class.assertEqual(created_object.label, expected_label)
    test_class.assertEqual(created_object.language, expected_language)


class TestGraphDataTransformation(NoDatabaseTestCase):
    def test_get_value(self):
        expected_value = ['1234', 'Test', 'True', 'False', 'https://dwc.tdwg.org/terms/#family', 'Rot-Buche']
        run_subtests(self, data, expected_value, graph_data_transformations.get_value)

    def test_is_literal(self):
        expected_value = [True, True, True, True, False, True]
        run_subtests(self, data, expected_value, graph_data_transformations.is_literal)

    def test_get_label_and_language(self):
        expected_value = [
            ('1234', None),
            ('Test', None),
            ('True', None),
            ('False', None),
            (None, None),
            ('Rot-Buche', 'de')]

        transformer = graph_data_transformations.UriPropertyTransformation()
        run_subtests(self, graph_data, expected_value, transformer.get_label_and_language)

    def test_create_subject(self):
        transformer = graph_data_transformations.UriPropertyTransformation()
        subject_object = transformer.create_subject(create_objects_test_data)
        assert_object_correct(self, subject_object, graph_data_transformations.Subject,
                              expected_label=None,
                              expected_uri='http://purl.obolibrary.org/obo/bla',
                              expected_language=None)

    def test_create_predicate(self):
        transformer = graph_data_transformations.UriPropertyTransformation()
        subject_object = transformer.create_predicate(create_objects_test_data)
        assert_object_correct(self, subject_object, graph_data_transformations.Predicate,
                              expected_label='flower color',
                              expected_uri='https://www.biofid.de/bio-ontologies#has_petal_color',
                              expected_language='en')

    def test_create_object(self):
        transformer = graph_data_transformations.UriPropertyTransformation()
        subject_object = transformer.create_object(create_objects_test_data)
        assert_object_correct(self, subject_object, graph_data_transformations.Object,
                              expected_label='brown',
                              expected_uri='http://purl.obolibrary.org/obo/PATO_0000952',
                              expected_language=None)




