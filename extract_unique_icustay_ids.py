import argparse
import pandas as pd
import logging

from column_keys import ICU_STAY_ID_COLUMN_KEY


def extract_unique_icu_stay_ids(df_glucose_insulin: pd.DataFrame, argument_namespace: argparse.Namespace) -> [int]:
    """
    Extracts unique ICU stay identifiers from the glucose insulin dataset dataframe.
    :param df_glucose_insulin: The glucose insulin dataset dataframe.
    :param argument_namespace: The argument namespace.
    :return: A list of unique ICU stay identifiers.
    """
    ids: [int] = tuple(df_glucose_insulin[ICU_STAY_ID_COLUMN_KEY].unique())

    if argument_namespace.max > 0:
        return ids[:argument_namespace.max]

    return ids
