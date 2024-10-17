import logging
import pandas as pd

from curation.constants import ColumnKey
from selection.generate_df_dataset import generate_df_dataset
from selection.generate_hyperglycaemic_dataset import generate_hyperglycaemic_dataset
from .select_subjects import select_subjects

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    rule = "2h"

    df_glucose_insulin: pd.DataFrame
    df_demographics: pd.DataFrame
    df_prescriptions: pd.DataFrame
    df_labevents: pd.DataFrame

    df_glucose_insulin, df_demographics, df_prescriptions, df_labevents = (
        select_subjects(count=None)
    )

    identifier_columns: list[str] = [
        ColumnKey.SUBJECT_ID.value,
        ColumnKey.HOSPITAL_ADMISSION_ID.value,
        ColumnKey.ICU_STAY_ID.value,
    ]
    glucose_columns: list[str] = ["glc", "glcsource", "timer"]
    insulin_columns: list[str] = [
        "input_hrs",
        "insulintype",
        "event",
        "infxstop",
    ]
    demographics_columns: list[str] = [
        "age",
        "gender",
        "weight",
        "height",
    ]
    prescriptions_columns: list[str] = ["startdate", "enddate", "rxclass_ATC1-4_id"]

    labevents_columns: list[str] = [
        "subject_id",
        "hadm_id",
        "charttime",
        "COMPONENT",
        "PROPERTY",
        "SYSTEM",
        "TIME_ASPCT",
        "METHOD_TYP",
    ]

    df_dataset = generate_df_dataset(
        df_glucose_insulin=df_glucose_insulin,
        df_demographics=df_demographics,
        df_labevents=df_labevents,
        df_prescriptions=df_prescriptions,
        identifier_columns=identifier_columns,
        glucose_columns=glucose_columns,
        insulin_columns=insulin_columns,
        demographics_columns=demographics_columns,
        prescriptions_columns=prescriptions_columns,
        rule=rule,
    )
    df_hyperglycaemic_dataset = generate_hyperglycaemic_dataset(df_dataset=df_dataset)

    df_summary = pd.DataFrame(
        df_hyperglycaemic_dataset.isna().mean(), columns=["missing"]
    ).sort_values(by="missing", ascending=True)

    subject_ids = df_hyperglycaemic_dataset.index.get_level_values(
        ColumnKey.SUBJECT_ID.value
    ).unique()
    hadm_ids = df_hyperglycaemic_dataset.index.get_level_values(
        ColumnKey.HOSPITAL_ADMISSION_ID.value
    ).unique()
    icustay_ids = df_hyperglycaemic_dataset.index.get_level_values(
        ColumnKey.ICU_STAY_ID.value
    ).unique()

    exit(0)
