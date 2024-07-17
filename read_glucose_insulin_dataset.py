import numpy
import pandas as pd
import logging

from column_keys import ColumnKey
from extract_unique_icustay_ids import extract_unique_icu_stay_ids
from log_identifier_summary import log_identifier_summary

# The directory from the uncompressed .zip file contents.
GLUCOSE_INSULIN_REPOSITORY_DIRECTORY = (
    './../curated-data-for-describing-blood-glucose-management-in-the-intensive-care-unit-1.0.1'
)

# The filepath of the dataset .csv file in the dataset respository directory.
GLUCOSE_INSULIN_PAIR_FILEPATH = '/Datasets/glucose_insulin_pair.csv'

# The columns to sort the dataset by.
GLUCOSE_INSULIN_COLUMNS_TO_SORT: [str] = [
    ColumnKey.SUBJECT_ID.value,
    ColumnKey.HOSPITAL_ADMISSION_ID.value,
    ColumnKey.ICU_STAY_ID.value,
    ColumnKey.TIMER.value
]


def read_glucose_insulin_dataset(
        max_identifier_count: int
) -> tuple[
    pd.DataFrame,
    tuple[numpy.int64],
    tuple[numpy.int64],
    tuple[numpy.int64]
]:
    """
    Reads the 'Curated Data for Describing Blood Glucose Management in the Intensive Care Unit' dataset, specifically
    the file 'glucose_insulin_pair.csv'.
    :param max_identifier_count: The maximum number of unique ICU stay identifiers to extract.
    :return: The dataset as a dataframe, the unique ICU stay identifiers, the unique subject identifiers, and the unique
    hospital admission identifiers.
    """
    filepath = f"{GLUCOSE_INSULIN_REPOSITORY_DIRECTORY}/{GLUCOSE_INSULIN_PAIR_FILEPATH}"

    try:
        df_glucose_insulin: pd.DataFrame = pd.read_csv(filepath)

        # Convert the column names to lowercase.
        df_glucose_insulin.columns = map(str.lower, df_glucose_insulin.columns)

        logging.info(
            f"Successfully read {str(len(df_glucose_insulin))} rows from 'Curated Data for Describing Blood Glucose "
            f"Management in the Intensive Care Unit'."
        )

        # Sort the dataset by the sorted columns.
        df_glucose_insulin: pd.DataFrame = df_glucose_insulin.sort_values(
            by=GLUCOSE_INSULIN_COLUMNS_TO_SORT
        )

        # Extract unique identifiers for each ICU stay, and truncate the extraction if applicable.
        icu_stay_ids: tuple[numpy.int64] = extract_unique_icu_stay_ids(
            df_glucose_insulin=df_glucose_insulin,
            max_identifier_count=max_identifier_count
        )

        # Filter the glucose insulin dataset to only include the unique ICU stay identifiers.
        df_glucose_insulin = df_glucose_insulin[df_glucose_insulin[ColumnKey.ICU_STAY_ID.value].isin(icu_stay_ids)]

        # Extract the unique identifiers for each subject.
        subject_ids: tuple[numpy.int64] = tuple(df_glucose_insulin[ColumnKey.SUBJECT_ID.value].unique())

        # Extract the unique identifiers for each hospital admission.
        hospital_admission_ids: tuple[numpy.int64] = tuple(
            df_glucose_insulin[ColumnKey.HOSPITAL_ADMISSION_ID.value].unique())

        # Log the summary of unique identifiers.
        log_identifier_summary(icu_stay_ids=icu_stay_ids, subject_ids=subject_ids,
                               hospital_admission_ids=hospital_admission_ids)

        return df_glucose_insulin, icu_stay_ids, subject_ids, hospital_admission_ids
    except FileNotFoundError:
        logging.critical(
            f"The 'Curated Data for Describing Blood Glucose Management in the Intensive Care Unit' dataset could not "
            f"be found at {filepath}. Please ensure that the uncompressed .zip file contents from "
            f"https://physionet.org/content/glucose-management-mimic/1.0.1/#files-panel is in the same directory as "
            f"this repository.")

        exit(1)
