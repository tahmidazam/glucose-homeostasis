from curation.demographics.icd9_chapter import ICD9Chapter


def is_neoplasm_or_pregnancy(icd9_code) -> bool:
    if not icd9_code.isnumeric():
        return False

    try:
        prefix: int = int(icd9_code[:3])
        return prefix in ICD9Chapter.NEOPLASMS.value + ICD9Chapter.COMPLICATIONS_OF_PREGNANCY_CHILDBIRTH_AND_THE_PUERPERIUM.value
    except ValueError:
        return False
