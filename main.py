import argparse

import numpy
import pandas as pd
import sqlalchemy

from cli.define_arguments import define_arguments
from constants.column_keys import ColumnKey
from constants.filter import Filter
from constants.icd9_chapter import ICD9Chapter
from constants.table_name import TableName
from df_utils.calculate_age import calculate_age
from df_utils.generate_df_demographics import generate_df_demographics
from logging_utils.log_table_query_summary import log_table_query_summary
from query.query_heights_weights import query_heights_weights
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

    log_table_query_summary(
        df_admissions=df_admissions,
        df_patients=df_patients,
        df_diagnoses_icd=df_diagnoses_icd,
        df_icu_stays=df_icu_stays
    )

    # Generate the demographics dataframe from merging tables.
    df_demographics: pd.DataFrame = generate_df_demographics(
        df_icu_stays=df_icu_stays,
        df_admissions=df_admissions,
        df_patients=df_patients
    )

    # Calculate the age of the patients.
    df_demographics: pd.DataFrame = calculate_age(df_demographics)

    # Merge the demographics dataset with the ICU stay and subject identifiers from the glucose insulin dataset to
    # respect readmission.
    df_demographics = pd.merge(
        left=df_demographics,
        right=df_glucose_insulin[[ColumnKey.ICU_STAY_ID.value, ColumnKey.FIRST_ICU_STAY.value]],
        on=ColumnKey.ICU_STAY_ID.value, how='inner'
    ).drop_duplicates()

    # Filter the demographics dataframe by age.
    df_demographics: pd.DataFrame = df_demographics[
        (df_demographics[ColumnKey.AGE.value] > Filter.AGE_LOWER_BOUND.value) & (
                df_demographics[ColumnKey.AGE.value] < Filter.AGE_UPPER_BOUND.value)]

    # Filter the demographics dataframe by length of stay.
    df_demographics: pd.DataFrame = df_demographics[
        (df_demographics[ColumnKey.LENGTH_OF_STAY.value] > Filter.LENGTH_OF_STAY_LOWER_BOUND.value) & (
                df_demographics[ColumnKey.LENGTH_OF_STAY.value] < Filter.LENGTH_OF_STAY_UPPER_BOUND.value)]

    # Preserve relevant columns.
    relevant_columns: [ColumnKey] = [
        ColumnKey.SUBJECT_ID,
        ColumnKey.HOSPITAL_ADMISSION_ID,
        ColumnKey.ICU_STAY_ID,
        ColumnKey.IN_TIME,
        ColumnKey.DIAGNOSIS,
        ColumnKey.AGE,
        ColumnKey.GENDER,
    ]

    df_demographics = df_demographics[[k.value for k in relevant_columns]]

    # Query the heights and weights of the patients.
    df_heights_weights = query_heights_weights(
        engine=engine,
        subject_ids=subject_ids,
        chunk_size=main_argument_namespace.chunk_size
    )

    # Convert the chart time to a datetime type.
    df_heights_weights[ColumnKey.CHART_TIME.value] = pd.to_datetime(
        df_heights_weights[ColumnKey.CHART_TIME.value])

    # Forward- and back-fill weights and heights.
    df_heights_weights[ColumnKey.HEIGHT.value] = df_heights_weights.groupby(ColumnKey.ICU_STAY_ID.value)[
        ColumnKey.HEIGHT.value].ffill().bfill()

    df_heights_weights[ColumnKey.WEIGHT.value] = df_heights_weights.groupby(ColumnKey.ICU_STAY_ID.value)[
        ColumnKey.WEIGHT.value].ffill().bfill()

    # Take the last (i.e., most recent) height and weight for each ICU stay.
    df_heights_weights = df_heights_weights.groupby(ColumnKey.ICU_STAY_ID.value).last().reset_index()

    df_demographics = pd.merge(df_demographics, df_heights_weights,
                               on=[ColumnKey.SUBJECT_ID.value],
                               how='left')

    # Drop rows with missing height or weight.
    df_demographics.dropna(subset=[ColumnKey.HEIGHT.value, ColumnKey.WEIGHT.value], inplace=True)

    exit(0)
