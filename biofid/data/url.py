def is_url(string: str) -> bool:
    """ Tests if a given string is a URL. """
    return 'http' in string and '://' in string and '.' in string
