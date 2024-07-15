import argparse
import pandas as pd

from connect_to_local_mimic import connect_to_local_mimic
from define_arguments import define_arguments
from read_glucose_insulin_dataset import read_glucose_insulin_dataset

if __name__ == '__main__':
    # Define command-line arguments.
    main_argument_parser: argparse.ArgumentParser = define_arguments()

    # Attempt connection to the MIMIC-III Postgres database.
    mimic = connect_to_local_mimic(argument_parser=main_argument_parser)

    # Read the glucose insulin dataset.
    df_glucose_insulin: pd.DataFrame = read_glucose_insulin_dataset()
