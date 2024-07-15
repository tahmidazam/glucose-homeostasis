import argparse
import pandas as pd

from connect_to_local_mimic import connect_to_local_mimic
from define_arguments import define_arguments
from read_glucose_insulin_dataset import read_glucose_insulin_dataset

SUBJECT_ID_COLUMN_KEY: str = "SUBJECT_ID"
HADM_ID_COLUMN_KEY: str = "HADM_ID"
ICUSTAY_ID_COLUMN_KEY: str = "ICUSTAY_ID"
TIMER_COLUMN_KEY: str = "TIMER"

if __name__ == '__main__':
    # Define command-line arguments.
    main_argument_parser: argparse.ArgumentParser = define_arguments()
    main_argument_namespace: argparse.Namespace = main_argument_parser.parse_args()

    # Attempt connection to the MIMIC-III Postgres database.
    mimic = connect_to_local_mimic(argument_namespace=main_argument_namespace)

    # Reading and sorting of the glucose insulin dataset.
    glucose_insulin_sort_values: [str] = [SUBJECT_ID_COLUMN_KEY, HADM_ID_COLUMN_KEY, ICUSTAY_ID_COLUMN_KEY,
                                          TIMER_COLUMN_KEY]
    df_glucose_insulin: pd.DataFrame = read_glucose_insulin_dataset().sort_values(by=glucose_insulin_sort_values)

    # Extract unique identifiers for each ICU stay.
    all_icustay_ids: [str] = tuple(df_glucose_insulin[ICUSTAY_ID_COLUMN_KEY].unique())
