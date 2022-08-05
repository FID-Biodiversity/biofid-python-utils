from typing import Optional

from django.http import HttpRequest

ACCEPTED_SUFFIX_MAPPING = {
    'json': 'application/json',
    'html': 'application/html',
    'rdf': 'application/rdf+xml',
    'ttl': 'text/turtle'
}

ACCEPT_HEADER = 'HTTP_ACCEPT'


def modify_header_by_request_suffix(request: HttpRequest) -> None:
    """ Takes a HttpRequest objects and modifies the ACCEPTED header appropriate to the suffix in the URL.
        For example, a URL like 'https://www.example.com/uri.json' would set the ACCEPT header to 'application/json'.
        If no suffix is given, nothing happens.
    """

    requested_url = request.get_full_path()
    if has_url_accepted_suffix(requested_url):
        given_suffix = extract_suffix_from_string(requested_url)
        new_accepted_header = ACCEPTED_SUFFIX_MAPPING.get(given_suffix, ACCEPTED_SUFFIX_MAPPING['html'])
        request.META[ACCEPT_HEADER] = new_accepted_header


def has_url_accepted_suffix(url: str) -> bool:
    """ Tests if a given URL has a acceptable suffix.
        Example:    'https://www.example.com/uri.json'  returns True,
                    'https://www.example.com/uri'       returns False
    """
    suffix = extract_suffix_from_string(url)
    return False if suffix is None else suffix in ACCEPTED_SUFFIX_MAPPING


def extract_suffix_from_string(text: str) -> Optional[str]:
    """ Returns a suffix of any kind given in a text.
        Only the suffix is returned. The leading period is skipped!
        Returns None, if no suffix is present.
    """
    suffix = text.rsplit('.', maxsplit=1)
    return suffix[-1] if suffix else None
