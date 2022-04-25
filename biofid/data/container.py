from typing import Any, Collection, Generator, Iterable, Type, Callable


def convert_all_container_recursively(container: Iterable, conversion_type: Type) -> Any:
    """ Converts all containers within a given container into the given conversion type.
        This process is recursive! The parent container itself is ALSO converted!
    """
    if is_container(container):
        result = conversion_type(convert_all_container_recursively(elem, conversion_type) for elem in container)
        return result
    else:
        return container


def group_elements(container: Iterable, group_size: int):
    """ Groups multiple adjacent elements from a container per loop. """
    return zip(*[iter(container)] * group_size)


def is_container(element: Any) -> bool:
    """ Checks that the given element is an Iterable, but not a string. """
    return not isinstance(element, str) and isinstance(element, Iterable)


def iterate_recursively(container: Collection[Any]) -> Generator:
    """ Returns a generator that all elements in the given container recursively in order. """
    for element in container:
        if is_container(element):
            yield from iterate_recursively(element)
        else:
            yield element


def escape_keys_and_values_of_dict(dict_to_escape: dict, escaping_function: Callable) -> dict:
    """ Returns a new dict in which all keys and values are escaped by the given escape function.
        All iterables that are not dicts are returned as lists.
    """
    new_dict = {}
    for key, value in dict_to_escape.items():
        escaped_key = escaping_function(key)

        if isinstance(value, dict):
            escaped_value = escape_keys_and_values_of_dict(value, escaping_function)
        elif is_container(value):
            escaped_value = escape_list(value, escaping_function)
        else:
            escaped_value = escaping_function(value)

        new_dict[escaped_key] = escaped_value

    return new_dict


def escape_list(list_to_escape: list, escaping_function: Callable) -> list:
    """ Escapes all elements of a (nested) list. """
    return [escape_list(elem, escaping_function) if is_container(elem) else escaping_function(elem)
            for elem in list_to_escape]
