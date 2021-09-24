from typing import Any, Collection, Generator, Iterable


def iterate_recursively(container: Collection[Any]) -> Generator:
    """ Returns a generator that all elements in the given container recursively in order. """
    for element in container:
        if isinstance(element, Collection) and not isinstance(element, str):
            yield from iterate_recursively(element)
        else:
            yield element


def is_container(element: Any) -> bool:
    """ Checks that the given element is an Iterable, but not a string. """
    return not isinstance(element, str) and isinstance(element, Iterable)
