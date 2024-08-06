import numpy as np

from curation.prescriptions.find_rxcui_by_id import FindRxCUIByIDResponse, find_rxcui_by_id, IdType


def identify_drug_using_ndc(row):
    ndc_raw_value: str = row['ndc']

    # If the NDC is '0' or None, return the row.
    if ndc_raw_value == '0' or ndc_raw_value is None:
        return row

    ndcs: list[str] = ndc_raw_value.split(' ')
    rxcuis_2d: list[list[int]] = []

    # Find the RxCUIs for the NDC using RxNorm.
    for ndc in ndcs:
        find_rxcui_by_id_response: FindRxCUIByIDResponse = find_rxcui_by_id(id_type=IdType.NDC, id=ndc_raw_value)
        rxcuis_2d.append(find_rxcui_by_id_response.id_group.rxnorm_id)

    # Extract the RxCUIs from the response.
    rxcuis = np.concatenate(rxcuis_2d)

    # If there are no RxCUIs, return the row.
    if len(rxcuis) == 0:
        return row

    # Extract the first RxCUI.
    rxcui = rxcuis[0]

    # Add the RxCUI to the row.
    row[ColumnKey.RXCUI.value] = rxcui

    return row
