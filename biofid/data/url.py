import re


def is_url(string: str) -> bool:
    """ Tests if a given string is a URL. """
    string = string.strip()

    localhost_regex = re.search(r'^http://localhost[/:][a-zA-Z0-9/]*$', string)

    if localhost_regex is not None:
        return True

    return re.search(r'(?:^https?://(?:www.)?|^www\.)[a-zA-Z\-]+?\.[a-z]{2,5}(?:/[a-zA-Z0-9]*)?/?$', string) is not None
