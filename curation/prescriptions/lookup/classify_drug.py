from curation.prescriptions.get_class_by_rxcui import GetClassByRxCUIResponse, get_class_by_rxcui


def classify_drug(row):
    """
    Classify the drug in the row using the RxCUI.
    :param row: The row to classify.
    :return: The row with the drug classified, with additional columns for each class type.
    """
    # Extract the first RxCUI.
    rxcui = row['rxcui']

    # If the RxCUI is None, return the row.
    if rxcui is None:
        return row

    # Get the drug classes for the RxCUI using RxClass.
    get_class_by_rxcui_response: GetClassByRxCUIResponse = get_class_by_rxcui(rxcui=rxcui)

    # Extract the drug classes from the response and add them to the row.
    for element in get_class_by_rxcui_response.rxclass_drug_info_list.rxclass_drug_info:
        row[f"rxclass_{element.rxclass_min_concept_item.class_type}_id"] = element.rxclass_min_concept_item.class_id
        row[f"rxclass_{element.rxclass_min_concept_item.class_type}_name"] = element.rxclass_min_concept_item.class_name

    return row
