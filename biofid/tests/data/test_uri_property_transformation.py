from biofid.data.transformation.graph_data_transformations import UriPropertyTransformation, Predicate, Object
from biofid.tests.base import NoDatabaseTestCase

label_data = [
    {"object": {"type": "uri", "value": "http://purl.obolibrary.org/obo/FLOPO_0009779"},
     "objectLabel": {"type": "literal", "value": "flower brown"}},
    {"predicate": {"type": "uri", "value": "https://www.biofid.de/bio-ontologies#has_petal_color"},
     "predicateLabel": {"type": "literal", "value": "flower color"}},
    {"predicate": {"type": "uri", "value": "https://dwc.tdwg.org/terms/#vernacularName"}},
    {"object": {"type": "literal", "xml:lang": "de", "value": "Rotbuche"}},
    {"object": {"type": "typed-literal", "datatype": "http://www.w3.org/2001/XMLSchema#string",
                "value": "23906"}}
]

expected_labels_and_languages = [
    ('flower brown', None), ('flower color', None), (None, None), ('Rotbuche', 'de'), ('23906', None)
]

predicate_data = [
    {"predicate": {"type": "uri", "value": "https://www.biofid.de/bio-ontologies#has_petal_color"},
     "predicateLabel": {"type": "literal", "value": "flower color"}},
    {"predicate": {"type": "uri", "value": "https://dwc.tdwg.org/terms/#vernacularName"}},
]

expected_predicate_instances = [
    Predicate(label='flower color', language=None, uri='https://www.biofid.de/bio-ontologies#has_petal_color'),
    Predicate(label=None, language=None, uri='https://dwc.tdwg.org/terms/#vernacularName')
]

object_data = [
    {"object": {"type": "uri", "value": "http://purl.obolibrary.org/obo/FLOPO_0009779"},
     "objectLabel": {"type": "literal", "value": "flower brown"}},
    {"object": {"type": "literal", "xml:lang": "de", "value": "Rotbuche"}},
]

expected_object_instances = [
    Object(label='flower brown', language=None, uri='http://purl.obolibrary.org/obo/FLOPO_0009779'),
    Object(label='Rotbuche', language='de', uri=None)
]


class TestUriPropertyTransformation(NoDatabaseTestCase):
    def test_predicate_label_and_language_extraction(self):
        for input_data, expected_label_and_language in zip(label_data, expected_labels_and_languages):
            with self.subTest():
                self.assertEquals(UriPropertyTransformation().get_label_and_language(input_data),
                                  expected_label_and_language)

    def test_predicate_creation(self):
        for input_data, expected_instance in zip(predicate_data, expected_predicate_instances):
            with self.subTest():
                predicate = UriPropertyTransformation().create_predicate(input_data)
                self.assertEquals(predicate, expected_instance)
                self.assertTrue(isinstance(predicate, Predicate))

    def test_object_creation(self):
        for input_data, expected_instance in zip(object_data, expected_object_instances):
            with self.subTest():
                object_instance = UriPropertyTransformation().create_object(input_data)
                self.assertEquals(object_instance, expected_instance)
                self.assertTrue(isinstance(object_instance, Object))
