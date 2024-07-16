import argparse
import logging

import pandas as pd
from tabulate import tabulate

from column_keys import SUBJECT_ID_COLUMN_KEY, HOSPITAL_ADMISSION_ID_COLUMN_KEY, ICU_STAY_ID_COLUMN_KEY, \
    TIMER_COLUMN_KEY
from connect_to_local_mimic import connect_to_local_mimic
from define_arguments import define_arguments
from extract_unique_icustay_ids import extract_unique_icu_stay_ids
from log_identifier_summary import log_identifier_summary
from read_glucose_insulin_dataset import read_glucose_insulin_dataset
from set_log_level import set_log_level

if __name__ == '__main__':
    # Define command-line arguments.
    main_argument_parser: argparse.ArgumentParser = define_arguments()
    main_argument_namespace: argparse.Namespace = main_argument_parser.parse_args()

    # Attempt connection to the MIMIC-III Postgres database.
    mimic = connect_to_local_mimic(argument_namespace=main_argument_namespace)

    # Set log level based on argument namespace.
    set_log_level(argument_namespace=main_argument_namespace)

    # Reading and sorting of the glucose insulin dataset.
    glucose_insulin_sort_values: [str] = [SUBJECT_ID_COLUMN_KEY, HOSPITAL_ADMISSION_ID_COLUMN_KEY,
                                          ICU_STAY_ID_COLUMN_KEY, TIMER_COLUMN_KEY]
    df_glucose_insulin: pd.DataFrame = read_glucose_insulin_dataset().sort_values(by=glucose_insulin_sort_values)

    # Extract unique identifiers for each ICU stay, and truncate the extraction if applicable.
    icu_stay_ids: [int] = extract_unique_icu_stay_ids(df_glucose_insulin=df_glucose_insulin,
                                                      argument_namespace=main_argument_namespace)

    # Filter the glucose insulin dataset to only include the unique ICU stay identifiers.
    df_glucose_insulin = df_glucose_insulin[df_glucose_insulin[ICU_STAY_ID_COLUMN_KEY].isin(icu_stay_ids)]

    # Extract the unique identifiers for each subject.
    subject_ids: [int] = tuple(df_glucose_insulin[SUBJECT_ID_COLUMN_KEY].unique())

    # Extract the unique identifiers for each hospital admission.
    hospital_admission_ids: [int] = tuple(df_glucose_insulin[HOSPITAL_ADMISSION_ID_COLUMN_KEY].unique())

    # Log the summary of unique identifiers.
    log_identifier_summary(icu_stay_ids=icu_stay_ids, subject_ids=subject_ids,
                           hospital_admission_ids=hospital_admission_ids)

    exit(0)
