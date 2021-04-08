def traverse(obj, tree_types=(list, tuple)):
    """ Iterates a (recursively) nested list and returns a single list over all elements.
        If the given list is not nested, nothing happens.
        Source: https://stackoverflow.com/a/6340578/7504509
    """
    if isinstance(obj, tree_types):
        for value in obj:
            for subvalue in traverse(value, tree_types):
                yield subvalue
    else:
        yield obj
