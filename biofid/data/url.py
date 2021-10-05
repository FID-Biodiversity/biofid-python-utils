import re


def is_url(string: str) -> bool:
    """ Tests if a given string is a URL.
        If the given string is not a string, False is returned.
    """
    if not isinstance(string, str):
        return False

    string = string.strip()

    localhost_regex = re.search(r'^http://localhost[/:][a-zA-Z0-9/]*$', string)

    if localhost_regex is not None:
        return True

    url_regex = r'(?:^https?://(?:[sw]w[sw].)?|^www\.)[a-zA-Z-\.]+?\.[a-z]{2,5}' \
                r'(?:/[a-zA-Z0-9/\-#_]*\.?[a-z]*|\.[a-z]+?)?/?$'

    return re.search(url_regex, string) is not None
