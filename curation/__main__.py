import argparse

import numpy
import pandas as pd
import sqlalchemy
from dotenv import dotenv_values

from config import config_from_dict, config_to_mimic_db_url
from define_arguments import define_arguments
from set_log_level import set_log_level
from verify_cache_directory import verify_cache_directory
from .demographics import generate_df_demographics
from .prescriptions import generate_df_prescriptions
from .read_glucose_insulin_dataset import read_glucose_insulin_dataset

if __name__ == '__main__':
    # Define command-line arguments.
    main_argument_parser: argparse.ArgumentParser = define_arguments()
    main_argument_namespace: argparse.Namespace = main_argument_parser.parse_args()

    # Read environment variables.
    config = config_from_dict(dotenv_values())

    # Create reference to MIMIC-III Postgres database.
    url: str = config_to_mimic_db_url(config=config)
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

    # Generate the demographics dataframe from the queried tables.
    df_demographics: pd.DataFrame = generate_df_demographics(
        engine=engine,
        df_glucose_insulin=df_glucose_insulin,
        subject_ids=subject_ids,
        main_argument_namespace=main_argument_namespace,
        icu_stay_ids=icu_stay_ids
    )

    df_prescriptions: pd.DataFrame = generate_df_prescriptions(
        engine=engine,
    )

    exit(0)
