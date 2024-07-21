from enum import Enum


class TableName(Enum):
    ADMISSIONS: str = "ADMISSIONS"
    CALLOUT: str = "CALLOUT"
    CAREGIVERS: str = "CAREGIVERS"
    CHARTEVENTS: str = "CHARTEVENTS"
    CPTEVENTS: str = "CPTEVENTS"
    D_CPT: str = "D_CPT"
    D_ICD_DIAGNOSES: str = "D_ICD_DIAGNOSES"
    D_ICD_PROCEDURES: str = "D_ICD_PROCEDURES"
    D_ITEMS: str = "D_ITEMS"
    D_LABITEMS: str = "D_LABITEMS"
    DATETIMEEVENTS: str = "DATETIMEEVENTS"
    DIAGNOSES_ICD: str = "DIAGNOSES_ICD"
    DRGCODES: str = "DRGCODES"
    ICUSTAYS: str = "ICUSTAYS"
    INPUTEVENTS_CV: str = "INPUTEVENTS_CV"
    INPUTEVENTS_MV: str = "INPUTEVENTS_MV"
    OUTPUTEVENTS: str = "OUTPUTEVENTS"
    LABEVENTS: str = "LABEVENTS"
    MICROBIOLOGYEVENTS: str = "MICROBIOLOGYEVENTS"
    NOTEEVENTS: str = "NOTEEVENTS"
    PATIENTS: str = "PATIENTS"
    PRESCRIPTIONS: str = "PRESCRIPTIONS"
    PROCEDUREEVENTS_MV: str = "PROCEDUREEVENTS_MV"
    PROCEDURES_ICD: str = "PROCEDURES_ICD"
    SERVICES: str = "SERVICES"
    TRANSFERS: str = "TRANSFERS"

    # Custom table names (i.e., from calculation or processing).
    CONVERTED_VALUES: str = "CONVERTED_VALUES"
