from pathlib import Path

import logging
import pandas as pd

from curation.constants import ColumnKey
from curation.read_glucose_insulin_dataset import (
    GLUCOSE_INSULIN_REPOSITORY_DIRECTORY,
    GLUCOSE_INSULIN_PAIR_FILEPATH,
)


def select_subjects(count: int | None = 10):
    path_df_selected_demographics = Path("./../df_cache/df_selected_demographics")
    path_df_selected_prescriptions = Path(
        "./../df_cache/df_selected_classified_prescriptions"
    )
    path_df_selected_labitems = Path("./../df_cache/df_selected_classified_labevents")
    path_df_selected_glucose_insulin = Path("./../df_cache/df_selected_glucose_insulin")
    path_df_glucose_insulin = Path(
        f"{GLUCOSE_INSULIN_REPOSITORY_DIRECTORY}/{GLUCOSE_INSULIN_PAIR_FILEPATH}"
    )
    path_df_demographics = Path("./../df_cache/df_demographics")
    path_df_prescriptions = Path("./../df_cache/df_classified_prescriptions")
    path_df_labitems = Path("./../df_cache/df_classified_labevents")

    if not count:
        df_demographics = pd.read_feather(path_df_demographics)

        subject_ids = df_demographics[ColumnKey.SUBJECT_ID.value].unique()
        icustay_ids = df_demographics[ColumnKey.ICU_STAY_ID.value].unique()
        hadm_ids = df_demographics[ColumnKey.HOSPITAL_ADMISSION_ID.value].unique()

        df_glucose_insulin: pd.DataFrame = pd.read_csv(path_df_glucose_insulin)
        df_glucose_insulin.columns = map(str.lower, df_glucose_insulin.columns)

        df_glucose_insulin = df_glucose_insulin[
            df_glucose_insulin[ColumnKey.SUBJECT_ID.value].isin(subject_ids)
            & df_glucose_insulin[ColumnKey.ICU_STAY_ID.value].isin(icustay_ids)
            & df_glucose_insulin[ColumnKey.HOSPITAL_ADMISSION_ID.value].isin(hadm_ids)
        ]

        df_prescriptions = pd.read_feather(path_df_prescriptions)
        df_labitems = pd.read_feather(path_df_labitems)

        return df_glucose_insulin, df_demographics, df_prescriptions, df_labitems

    # Return cached dataframes if they all exist.
    if (
        path_df_selected_demographics.is_file()
        and path_df_selected_prescriptions.is_file()
        and path_df_selected_labitems.is_file()
        and path_df_selected_glucose_insulin.is_file()
    ):
        df_demographics = pd.read_feather(path_df_selected_demographics)
        df_prescriptions = pd.read_feather(path_df_selected_prescriptions)
        df_labitems = pd.read_feather(path_df_selected_labitems)
        df_glucose_insulin = pd.read_feather(path_df_selected_glucose_insulin)

        return df_glucose_insulin, df_demographics, df_prescriptions, df_labitems

    # Check if the dataframes have been created by the curation module.
    if not (
        path_df_demographics.is_file()
        and path_df_prescriptions.is_file()
        and path_df_labitems.is_file()
    ):
        logging.critical(
            "Please run curation/__main__.py before running selection/__main__.py"
        )

    # Read full dataframes from disk.
    df_glucose_insulin: pd.DataFrame = pd.read_csv(path_df_glucose_insulin)
    df_glucose_insulin.columns = map(str.lower, df_glucose_insulin.columns)

    df_demographics = pd.read_feather(path_df_demographics)
    df_prescriptions = pd.read_feather(path_df_prescriptions)
    df_labitems = pd.read_feather(path_df_labitems)

    # Select the first n unique subject identifiers.
    s_glucose_reading_counts = (
        df_glucose_insulin.dropna(subset=["glc"])[ColumnKey.SUBJECT_ID.value]
        .value_counts()
        .sort_values(ascending=False)
    )
    total_subjects = len(s_glucose_reading_counts)
    midpoint = total_subjects // 2
    half_count = count // 2
    start = max(midpoint - half_count, 0)
    end = min(midpoint + half_count + (count % 2), total_subjects)

    subject_ids = s_glucose_reading_counts.iloc[start:end].index.tolist()

    # Filter dataframes by selected subject identifiers.
    df_demographics = df_demographics[
        df_demographics[ColumnKey.SUBJECT_ID.value].isin(subject_ids)
    ]
    df_prescriptions = df_prescriptions[
        df_prescriptions[ColumnKey.SUBJECT_ID.value].isin(subject_ids)
    ]
    df_labitems = df_labitems[df_labitems[ColumnKey.SUBJECT_ID.value].isin(subject_ids)]
    df_glucose_insulin = df_glucose_insulin[
        df_glucose_insulin[ColumnKey.SUBJECT_ID.value].isin(subject_ids)
    ]

    # Cache dataframes to disk.
    df_glucose_insulin.to_feather(path_df_selected_glucose_insulin)
    df_demographics.to_feather(path_df_selected_demographics)
    df_prescriptions.to_feather(path_df_selected_prescriptions)
    df_labitems.to_feather(path_df_selected_labitems)

    # Return dataframes filtered by selected subject identifiers.
    return (
        df_glucose_insulin,
        df_demographics,
        df_prescriptions,
        df_labitems,
    )
