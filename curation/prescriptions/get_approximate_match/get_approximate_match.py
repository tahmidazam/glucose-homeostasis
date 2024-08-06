from urllib.parse import quote

import requests

from .get_approximate_match_response import GetApproximateMatchResponse, get_approximate_match_response_from_dict


def get_approximate_match(term: str, max_entries: int = 20, option: bool = False, host: str = 'localhost',
                          port: int = 4000) -> GetApproximateMatchResponse:
    url: str = (
        f"http://{host}:{port}/REST/approximateTerm.json?term={quote(term)}&maxEntries={max_entries}&option={1 if option else 0}"
    )

    response = requests.get(url=url)
    json = response.json()

    return get_approximate_match_response_from_dict(json)
