import argparse

import pandas as pd

from column_keys import SUBJECT_ID_COLUMN_KEY, HADM_ID_COLUMN_KEY, ICUSTAY_ID_COLUMN_KEY, TIMER_COLUMN_KEY
from connect_to_local_mimic import connect_to_local_mimic
from define_arguments import define_arguments
from extract_unique_icustay_ids import extract_unique_icustay_ids
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
    glucose_insulin_sort_values: [str] = [SUBJECT_ID_COLUMN_KEY, HADM_ID_COLUMN_KEY, ICUSTAY_ID_COLUMN_KEY,
                                          TIMER_COLUMN_KEY]
    df_glucose_insulin: pd.DataFrame = read_glucose_insulin_dataset().sort_values(by=glucose_insulin_sort_values)

    # Extract unique identifiers for each ICU stay.
    all_icustay_ids: [str] = extract_unique_icustay_ids(df_glucose_insulin=df_glucose_insulin)

    exit(0)
