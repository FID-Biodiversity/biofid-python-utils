from typing import Any, Collection, Generator


def iterate_recursively(container: Collection[Any]) -> Generator:
    """ Returns a generator that all elements in the given container recursively in order. """
    for element in container:
        if isinstance(element, Collection) and not isinstance(element, str):
            yield from iterate_recursively(element)
        else:
            yield element
