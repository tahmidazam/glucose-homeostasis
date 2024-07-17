from enum import Enum


class ColumnKey(Enum):
    SUBJECT_ID: str = "subject_id"
    HOSPITAL_ADMISSION_ID: str = "hadm_id"
    ICU_STAY_ID: str = "icustay_id"
    TIMER: str = "timer"
    IN_TIME: str = "intime"
    DATE_OF_BIRTH: str = "dob"
    LENGTH_OF_STAY: str = "los"

    # Custom column keys (i.e., from calculation or processing).
    AGE: str = "age"
