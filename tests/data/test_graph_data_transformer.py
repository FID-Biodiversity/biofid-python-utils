from biofid.data.transformation import DataTransformer
from biofid.data.transformation.graph_data_transformations import UriPropertyTransformation, Triple, Predicate, \
    Object
from biofid.tests.base import NoDatabaseTestCase

graph_response_data = {
    'uri': 'http://www.example.com/foo',
    'data': [
    {"predicate": {"type": "uri", "value": "https://www.biofid.de/bio-ontologies#has_petal_color"},
     "object": {"type": "uri", "value": "http://purl.obolibrary.org/obo/PATO_0000952"},
     "predicateLabel": {"type": "literal", "value": "flower color"},
     "objectLabel": {"type": "literal", "value": "brown"}},
    {"predicate": {"type": "uri", "value": "https://www.biofid.de/bio-ontologies#try_accspeciesid"},
     "object": {"type": "typed-literal", "datatype": "http://www.w3.org/2001/XMLSchema#string",
                "value": "23906"}},
    ]
}

expected_triples = [
            Triple(
                subject=None,
                predicate=Predicate(label='flower color', language=None, 
                                    uri='https://www.biofid.de/bio-ontologies#has_petal_color'),
                object=Object(label='brown', language=None, 
                              uri='http://purl.obolibrary.org/obo/PATO_0000952')),
            Triple(
                subject=None,
                predicate=Predicate(label=None, language=None, 
                                    uri='https://www.biofid.de/bio-ontologies#try_accspeciesid'),
                object=Object(label='23906', language=None, uri=None)
            )
        ]


class TestGraphDataTransformer(NoDatabaseTestCase):
    def test_uri_property_transformation(self):
        property_data = DataTransformer.transform(graph_response_data, UriPropertyTransformation)

        self.assertEqual(len(property_data), 2)
        self.assertEqual(property_data, expected_triples)
