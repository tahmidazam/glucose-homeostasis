from enum import Enum


class ColumnKey(Enum):
    SUBJECT_ID: str = "subject_id"
    HOSPITAL_ADMISSION_ID: str = "hadm_id"
    ICU_STAY_ID: str = "icustay_id"
    TIMER: str = "timer"
    IN_TIME: str = "intime"
    DATE_OF_BIRTH: str = "dob"
    LENGTH_OF_STAY: str = "los"
    VALUE_NUMERICAL: str = "valuenum"
    CHART_TIME: str = "charttime"
    ITEM_ID: str = "itemid"
    SEQ_NUM: str = "seq_num"
    ICD9_CODE: str = "icd9_code"
    FIRST_ICU_STAY: str = "first_icu_stay"
    DIAGNOSIS: str = "diagnosis"
    GENDER: str = "gender"
    DRUG: str = "drug"
    DRUG_NAME_GENERIC = "drug_name_generic"

    # Custom column keys (i.e., from calculation or processing).
    AGE: str = "age"
    HEIGHT: str = "height"
    WEIGHT: str = "weight"
