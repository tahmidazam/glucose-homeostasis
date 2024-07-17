import argparse
import numpy
import pandas as pd
import sqlalchemy

from column_keys import ColumnKey
from define_arguments import define_arguments
from query_tables import query_tables
from read_glucose_insulin_dataset import read_glucose_insulin_dataset
from set_log_level import set_log_level
from url_from_argument_namespace import url_from_argument_namespace


def generate_df_demographics(
        df_icu_stays: pd.DataFrame,
        df_admissions: pd.DataFrame,
        df_patients: pd.DataFrame
) -> pd.DataFrame:
    """
    Generates a dataframe containing the demographics of the patients in the ICU stays.
    :param df_icu_stays: The ICU stays dataframe.
    :param df_admissions: The admissions dataframe.
    :param df_patients: The patients dataframe.
    :return:
    """
    return pd.merge(
        left=pd.merge(
            left=df_icu_stays,
            right=df_admissions,
            on=[
                ColumnKey.HOSPITAL_ADMISSION_ID.value,
                ColumnKey.SUBJECT_ID.value
            ],
            how='inner'
        ),
        right=df_patients,
        on=ColumnKey.SUBJECT_ID.value,
        how='inner'
    )
