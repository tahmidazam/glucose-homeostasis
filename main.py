import argparse

import numpy
import pandas as pd
import sqlalchemy

from cli.define_arguments import define_arguments
from constants.column_keys import ColumnKey
from constants.table_name import TableName
from generate_df_demographics import generate_df_demographics
from query.query_table import query_table
from query.read_glucose_insulin_dataset import read_glucose_insulin_dataset
from logging_utils.set_log_level import set_log_level
from db_connection.url_from_argument_namespace import url_from_argument_namespace
from query.verify_cache_directory import verify_cache_directory

if __name__ == '__main__':
    # Define command-line arguments.
    main_argument_parser: argparse.ArgumentParser = define_arguments()
    main_argument_namespace: argparse.Namespace = main_argument_parser.parse_args()

    # Create reference to MIMIC-III Postgres database.
    url: str = url_from_argument_namespace(argument_namespace=main_argument_namespace)
    engine: sqlalchemy.Engine = sqlalchemy.create_engine(url=url, execution_options={'stream_results': True})

    # Set log level.
    set_log_level(level=main_argument_namespace.log_level)

    # Create cache directory if it does not exist.
    verify_cache_directory()

    # Reading, sort and extract unique identifiers from the glucose insulin dataset.
    df_glucose_insulin: pd.DataFrame
    icu_stay_ids: tuple
    subject_ids: tuple
    hospital_admission_ids: tuple[numpy.int64]

    df_glucose_insulin, icu_stay_ids, subject_ids, hospital_admission_ids = read_glucose_insulin_dataset(
        max_identifier_count=main_argument_namespace.max_identifier_count
    )

    # Query the database tables, filtering by the appropriate unique identifiers.
    df_admissions: pd.DataFrame = query_table(
        engine=engine,
        table_name=TableName.ADMISSIONS,
        id_column_key=ColumnKey.SUBJECT_ID,
        ids=subject_ids,
        chunk_size=main_argument_namespace.chunk_size,
    )

    df_patients: pd.DataFrame = query_table(
        engine=engine,
        table_name=TableName.PATIENTS,
        id_column_key=ColumnKey.SUBJECT_ID,
        ids=subject_ids,
        chunk_size=main_argument_namespace.chunk_size,
    )

    df_icu_stays: pd.DataFrame = query_table(
        engine=engine,
        table_name=TableName.ICUSTAYS,
        id_column_key=ColumnKey.ICU_STAY_ID,
        ids=icu_stay_ids,
        chunk_size=main_argument_namespace.chunk_size,
    )

    df_diagnoses_icd: pd.DataFrame = query_table(
        engine=engine,
        table_name=TableName.DIAGNOSES_ICD,
        id_column_key=ColumnKey.SUBJECT_ID,
        ids=subject_ids,
        chunk_size=main_argument_namespace.chunk_size,
    )

    # Generate the demographics dataframe from the queried tables.
    df_demographics: pd.DataFrame = generate_df_demographics(
        engine=engine,
        df_glucose_insulin=df_glucose_insulin,
        df_icu_stays=df_icu_stays,
        df_admissions=df_admissions,
        df_patients=df_patients,
        df_diagnoses_icd=df_diagnoses_icd,
        subject_ids=subject_ids,
        chunk_size=main_argument_namespace.chunk_size
    )

    exit(0)
