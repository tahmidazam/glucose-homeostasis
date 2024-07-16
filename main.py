import argparse

import numpy
import pandas as pd
import sqlalchemy

from column_keys import SUBJECT_ID_COLUMN_KEY, HOSPITAL_ADMISSION_ID_COLUMN_KEY, ICU_STAY_ID_COLUMN_KEY, \
    TIMER_COLUMN_KEY
from define_arguments import define_arguments
from extract_unique_icustay_ids import extract_unique_icu_stay_ids
from log_identifier_summary import log_identifier_summary
from query_table import query_table
from read_glucose_insulin_dataset import read_glucose_insulin_dataset
from set_log_level import set_log_level
from url_from_argument_namespace import url_from_argument_namespace

if __name__ == '__main__':
    # Define command-line arguments.
    main_argument_parser: argparse.ArgumentParser = define_arguments()
    main_argument_namespace: argparse.Namespace = main_argument_parser.parse_args()

    # Attempt connection to the MIMIC-III Postgres database.
    engine: sqlalchemy.Engine = sqlalchemy.create_engine(
        url_from_argument_namespace(argument_namespace=main_argument_namespace)
    )

    # Set log level.
    set_log_level(level=main_argument_namespace.log_level)

    # Reading and sorting of the glucose insulin dataset.
    glucose_insulin_sort_values: [str] = [
        SUBJECT_ID_COLUMN_KEY,
        HOSPITAL_ADMISSION_ID_COLUMN_KEY,
        ICU_STAY_ID_COLUMN_KEY,
        TIMER_COLUMN_KEY
    ]

    df_glucose_insulin: pd.DataFrame = read_glucose_insulin_dataset().sort_values(by=glucose_insulin_sort_values)

    # Extract unique identifiers for each ICU stay, and truncate the extraction if applicable.
    icu_stay_ids: [numpy.int64] = extract_unique_icu_stay_ids(
        df_glucose_insulin=df_glucose_insulin,
        max_identifier_count=main_argument_namespace.max_identifier_count
    )

    # Filter the glucose insulin dataset to only include the unique ICU stay identifiers.
    df_glucose_insulin = df_glucose_insulin[df_glucose_insulin[ICU_STAY_ID_COLUMN_KEY].isin(icu_stay_ids)]

    # Extract the unique identifiers for each subject.
    subject_ids: [numpy.int64] = tuple(df_glucose_insulin[SUBJECT_ID_COLUMN_KEY].unique())

    # Extract the unique identifiers for each hospital admission.
    hospital_admission_ids: [numpy.int64] = tuple(df_glucose_insulin[HOSPITAL_ADMISSION_ID_COLUMN_KEY].unique())

    # Log the summary of unique identifiers.
    log_identifier_summary(icu_stay_ids=icu_stay_ids, subject_ids=subject_ids,
                           hospital_admission_ids=hospital_admission_ids)

    # Query the database tables for the unique identifiers.
    df_admissions: pd.DataFrame = query_table(
        engine=engine,
        table_name="admissions",
        id_column_key=SUBJECT_ID_COLUMN_KEY,
        ids=subject_ids,
        chunk_size=main_argument_namespace.chunk_size,
        description="Querying admissions table"
    )

    df_patients: pd.DataFrame = query_table(
        engine=engine,
        table_name="patients",
        id_column_key=SUBJECT_ID_COLUMN_KEY,
        ids=subject_ids,
        chunk_size=main_argument_namespace.chunk_size,
        description="Querying patients table"
    )

    exit(0)
