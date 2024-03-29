import re

EXCLUDE_IN_SOLR_QUERY = ['qt=', 'stream.body', '/config', 'shards.qt=', 'fl=', '/update', 'shards=']
SOLR_SPECIAL_CHARACTERS = '&|+\\!(){}[\]*^~?:$='


def escape_solr_input(query: str, escape_characters: str = SOLR_SPECIAL_CHARACTERS) -> str:
    """ Escapes special characters used by Solr.

        Regex taken from: https://github.com/swistakm/solrq (BSD 3-Clause License)

        Copyright (c) 2015, Michał Jaworski
        All rights reserved.

        Redistribution and use in source and binary forms, with or without
        modification, are permitted provided that the following conditions are met:

        * Redistributions of source code must retain the above copyright notice, this
          list of conditions and the following disclaimer.

        * Redistributions in binary form must reproduce the above copyright notice,
          this list of conditions and the following disclaimer in the documentation
          and/or other materials provided with the distribution.

        * Neither the name of solrq nor the names of its
          contributors may be used to endorse or promote products derived from
          this software without specific prior written permission.

        THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
        AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
        IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
        DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
        FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
        DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
        SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
        CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
        OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
        OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
    """
    if isinstance(query, int):
        return query

    solr_special_characters = re.compile(rf'(?<!\\)(?P<specialCharacter>[{escape_characters}])')
    return solr_special_characters.sub(r'\\\g<specialCharacter>', query)


def is_solr_query_safe(query) -> bool:
    """ This simple function shall protect the database from injection attacks.
        For Solr: Relies on the tips given in https://github.com/dergachev/solr-security-proxy
    """

    lowered_query = query.lower()
    if any(evil.lower() in lowered_query for evil in EXCLUDE_IN_SOLR_QUERY):
        return False

    # Everything was fine
    return True


def escape_sparql_string(text: str) -> str:
    """ Escapes dangerous characters in the given text string.
        Escaped characters:
            * Single quotes
            * Double quotes
            * Backslashes
    """
    characters_to_escape = ['\\', '\'', '\"']  # backslash has to be the first escaped character!

    for char in characters_to_escape:
        text = text.replace(char, f'\\{char}')

    return text
