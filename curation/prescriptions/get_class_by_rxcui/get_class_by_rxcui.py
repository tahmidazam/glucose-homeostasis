import requests

from .get_class_by_rxcui_response import GetClassByRxCUIResponse, get_class_by_rx_cui_response_from_dict


def get_class_by_rxcui(rxcui: int, host: str = 'localhost', port: int = 4000) -> GetClassByRxCUIResponse:
    url: str = (
        f"http://{host}:{port}/REST/rxclass/class/byRxcui.json?rxcui={rxcui}"
    )

    response = requests.get(url=url)
    json = response.json()

    return get_class_by_rx_cui_response_from_dict(json)
