from curation.constants import ColumnKey
from curation.prescriptions.find_rxcui_by_id import FindRxCUIByIDResponse, find_rxcui_by_id, IdType


def identify_drug_using_gsn(row):
    gsn_raw_value: str = row['gsn']

    if gsn_raw_value is None:
        return row

    gsns: list[str] = filter(lambda x: x != '', gsn_raw_value.split(' '))
    rxcuis: list[int] = []

    for gsn in gsns:
        find_rxcui_by_id_response: FindRxCUIByIDResponse = find_rxcui_by_id(id_type=IdType.GCN_SEQNO, id=gsn)
        rxcuis += find_rxcui_by_id_response.id_group.rxnorm_id

    if len(rxcuis) == 0:
        return row

    rxcui = rxcuis[0]
    row[ColumnKey.RXCUI.value] = rxcui

    return row
