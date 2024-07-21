import argparse
import logging

import numpy
import pandas as pd
import sqlalchemy
from matplotlib import pyplot as plt

from cli.define_arguments import define_arguments
from constants.column_keys import ColumnKey
from constants.filter_info import FilterInfo
from df_utils.calculate_age import calculate_age
from df_utils.generate_df_demographics import generate_df_demographics
from query.query_heights_weights import query_heights_weights
from query.query_tables import query_tables
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

    # Query the database tables, filtering by the unique identifiers
    df_admissions: pd.DataFrame
    df_patients: pd.DataFrame
    df_diagnoses_icd: pd.DataFrame
    df_icu_stays: pd.DataFrame

    df_admissions, df_patients, df_diagnoses_icd, df_icu_stays = query_tables(
        engine=engine,
        subject_ids=subject_ids,
        icu_stay_ids=icu_stay_ids,
        chunk_size=main_argument_namespace.chunk_size
    )

    # Generate the demographics dataframe from merging tables.
    df_demographics: pd.DataFrame = generate_df_demographics(
        df_icu_stays=df_icu_stays,
        df_admissions=df_admissions,
        df_patients=df_patients
    )

    # Calculate the age of the patients.
    df_demographics: pd.DataFrame = calculate_age(df_demographics)

    # Filter the demographics dataframe by age.
    df_demographics: pd.DataFrame = df_demographics[
        (df_demographics[ColumnKey.AGE.value] > FilterInfo.AGE_LOWER_BOUND.value) & (
                df_demographics[ColumnKey.AGE.value] < FilterInfo.AGE_UPPER_BOUND.value)]

    # Filter the demographics dataframe by length of stay.
    df_demographics: pd.DataFrame = df_demographics[
        (df_demographics[ColumnKey.LENGTH_OF_STAY.value] > FilterInfo.LENGTH_OF_STAY_LOWER_BOUND.value) & (
                df_demographics[ColumnKey.LENGTH_OF_STAY.value] < FilterInfo.LENGTH_OF_STAY_UPPER_BOUND.value)]

    # Query the heights and weights of the patients.
    df_heights_weights = query_heights_weights(
        engine=engine,
        subject_ids=subject_ids,
        chunk_size=main_argument_namespace.chunk_size
    )

    # Convert the chart time to a datetime type.
    df_heights_weights[ColumnKey.CHART_TIME.value] = pd.to_datetime(
        df_heights_weights[ColumnKey.CHART_TIME.value])

    x = df_heights_weights[df_heights_weights[ColumnKey.CHART_TIME.value].isnull()]

    # Forward- and back-fill weights and heights.
    df_heights_weights[ColumnKey.HEIGHT.value] = df_heights_weights.groupby(ColumnKey.ICU_STAY_ID.value)[
        ColumnKey.HEIGHT.value].ffill().bfill()

    df_heights_weights[ColumnKey.WEIGHT.value] = df_heights_weights.groupby(ColumnKey.ICU_STAY_ID.value)[
        ColumnKey.WEIGHT.value].ffill().bfill()

    # Take the last (i.e., most recent) height and weight for each ICU stay.
    df_heights_weights = pd.merge(df_glucose_insulin.sort_values(
        by=[ColumnKey.SUBJECT_ID.value, ColumnKey.ICU_STAY_ID.value, ColumnKey.TIMER.value], inplace=False).groupby(
        ColumnKey.ICU_STAY_ID.value).first().reset_index()[[ColumnKey.SUBJECT_ID.value, ColumnKey.ICU_STAY_ID.value]],
                                  df_heights_weights, on=[ColumnKey.ICU_STAY_ID.value, ColumnKey.SUBJECT_ID.value],
                                  how='left')

    df_heights_weights = df_heights_weights.dropna(subset=[ColumnKey.CHART_TIME.value])

    df_glucose_insulin_missing_heights_weights = df_heights_weights[
        df_heights_weights[ColumnKey.HEIGHT.value].isnull() | df_heights_weights[ColumnKey.WEIGHT.value].isnull()]

    exit(0)
