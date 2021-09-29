from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Type

from biofid.data.transformation.interfaces import DataTransformation


@dataclass
class GraphVariable:
    label: Optional[str]
    language: Optional[str]
    uri: Optional[str]

    def __hash__(self):
        return hash((self.label, self.language, self.uri))

    def __eq__(self, other):
        if isinstance(other, GraphVariable):
            return self.__hash__() == other.__hash__()
        else:
            return False


class Subject(GraphVariable):
    pass


class Predicate(GraphVariable):
    pass


class Object(GraphVariable):
    pass


@dataclass
class Triple:
    """ Holds a complete triple. """
    subject: Optional[Subject]
    predicate: Optional[Predicate]
    object: Optional[Object]

    def __hash__(self):
        return hash((self.subject, self.predicate, self.object))

    def __eq__(self, other):
        if isinstance(other, Triple):
            return self.__hash__() == other.__hash__()
        else:
            return False


def get_value(data: dict) -> Any:
    """ Returns the value of the given graph variable.
        Boolean Values are translated from "1" or "0" to "True" or "False", respectively.
        If the given data does not contain a "value" keyword, None is returned.
    """
    TRUE_STRING = 'True'
    FALSE_STRING = 'False'
    value_string = 'value'

    if data is None or value_string not in data:
        return None

    value = data[value_string]

    if is_boolean(data):
        return TRUE_STRING if bool(int(value)) else FALSE_STRING

    return value


def is_literal(data: dict) -> bool:
    """ Tests if a given graph variable is a literal. """
    return 'literal' in data.get('type', '')


def is_uri(data: dict) -> bool:
    """ Tests if a given graph variable is a URI. """
    return data.get('type') == 'uri'


def is_boolean(data: dict) -> bool:
    """ Tests if a given graph variable is a boolean value. """
    return data.get('datatype') == 'http://www.w3.org/2001/XMLSchema#boolean'


def get_all_data_with_keywords_containing(keyword_substring: str, data: dict) -> dict:
    return {key: value for key, value in data.items() if keyword_substring.lower() in key.lower()}


def get_language(data: dict) -> Optional[str]:
    return data.get('xml:lang')


class UriPropertyTransformation(DataTransformation):
    """ Transforms a graph database response into a list of UriProperty objects.
        The returned list is in the same order as the given list.
    """

    BOOLEAN_TRUE_TRANSLATION = 'Yes'
    BOOLEAN_FALSE_TRANSLATION = 'No'

    def transform(self, data: Optional[Dict[str, dict]]) -> List[Triple]:
        if data is None:
            return []

        graph_data = data['data']

        return [self.create_uri_property_from_data(uri_property) for uri_property in graph_data]

    def create_uri_property_from_data(self, data: dict) -> Triple:
        return Triple(
            subject=None,
            predicate=self.create_predicate(data),
            object=self.create_object(data)
        )

    def create_subject(self, data: dict) -> Subject:
        return self.create_variable_instance(data, 'subject', Subject)

    def create_predicate(self, data: dict) -> Predicate:
        return self.create_variable_instance(data, 'predicate', Predicate)

    def create_object(self, data: dict) -> Object:
        return self.create_variable_instance(data, 'object', Object)

    def create_variable_instance(self, data: dict, variable_name: str,
                                 variable_constructor: Type[GraphVariable]) -> GraphVariable:
        data = get_all_data_with_keywords_containing(variable_name, data)
        label, language = self.get_label_and_language(data)
        uri = self._get_uri(data)
        return variable_constructor(label=label, language=language, uri=uri)

    def get_label_and_language(self, data: dict) -> Tuple[Optional[str], Optional[str]]:
        """ Returns the label of the given data.
            Since it is not guaranteed that a graph variable has a label, any literal that can be
            found alternatively in the data is taken as label.
            If the given data is empty or None or no literal is given, a tuple with (None, None) is returned.
        """
        if data is None or not data:
            return None, None

        value_containing_label = self._get_data_containing_label(data)

        if value_containing_label is None:
            return None, None
        else:
            return get_value(value_containing_label), get_language(value_containing_label)

    def _get_data_containing_label(self, data: dict) -> Optional[dict]:
        for key in data.keys():
            if 'label' in key.lower():
                return data[key]

        for value in data.values():
            if is_literal(value):
                return value

        return None

    def _get_uri(self, data: dict) -> Optional[str]:
        for value in data.values():
            if is_uri(value):
                return get_value(value)

        return None
