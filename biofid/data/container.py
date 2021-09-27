from typing import Any, Collection, Generator, Iterable, Type


def iterate_recursively(container: Collection[Any]) -> Generator:
    """ Returns a generator that all elements in the given container recursively in order. """
    for element in container:
        if is_container(element):
            yield from iterate_recursively(element)
        else:
            yield element


def is_container(element: Any) -> bool:
    """ Checks that the given element is an Iterable, but not a string. """
    return not isinstance(element, str) and isinstance(element, Iterable)


def convert_all_container_recursively(container: Iterable, conversion_type: Type) -> Any:
    """ Converts all containers within a given container into the given conversion type.
        This process is recursive! The parent container itself is ALSO converted!
    """
    if is_container(container):
        result = conversion_type(convert_all_container_recursively(elem, conversion_type) for elem in container)
        return result
    else:
        return container
