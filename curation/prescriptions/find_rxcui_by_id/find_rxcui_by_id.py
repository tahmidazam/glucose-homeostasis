import requests

from .find_rxcui_by_id_response import find_rxcui_by_id_response_from_dict, FindRxCUIByIDResponse
from .id_type import IdType


def find_rxcui_by_id(
        id_type: IdType,
        id: str,
        all_src: bool = False,
        host: str = 'localhost',
        port: int = 4000,
) -> FindRxCUIByIDResponse:
    """
    Searches for an identifier (id parameter) from an RxNorm vocabulary indicated by idtype. The scope of the search
    is either Active concepts (allsrc=False) or Current concepts (allsrc=True).

    :param port: The port of the RxNorm API
    :param host: The host of the RxNorm API
    :param id_type: Type of identifier
    :param id: Identifier
    :param all_src: Scope of search
    :return: The RxCUIs of concepts associated with that identifier
    """
    url: str = (
        f"http://{host}:{port}/REST/rxcui.json?idtype={id_type.value}&id={id}&allsrc={1 if all_src else 0}"
    )

    response = requests.get(url=url)

    json = response.json()

    return find_rxcui_by_id_response_from_dict(json)
