import logging

import pandas as pd
from tabulate import tabulate

from table_name import TableName


def log_table_query_summary(
        df_admissions: pd.DataFrame,
        df_patients: pd.DataFrame,
        df_diagnoses_icd: pd.DataFrame,
        df_icu_stays: pd.DataFrame
):
    """
    Logs the count of rows in each dataframe.
    :param df_admissions: The admissions dataframe.
    :param df_patients: The patients dataframe.
    :param df_diagnoses_icd: The diagnoses_icd dataframe.
    :param df_icu_stays: The icu_stays dataframe.
    """
    table: str = tabulate(
        [
            [
                TableName.ADMISSIONS.value,
                len(df_admissions)
            ],
            [
                TableName.PATIENTS.value,
                len(df_patients)
            ],
            [
                TableName.DIAGNOSES_ICD.value,
                len(df_diagnoses_icd)
            ],
            [
                TableName.ICUSTAYS.value,
                len(df_icu_stays)
            ]
        ],
        headers=["Table", "Count"],
        tablefmt="pretty",
        colalign=("right", "left")
    )

    logging.info("\n" + table)
