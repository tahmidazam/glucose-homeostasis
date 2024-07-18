import pandas as pd

from constants.column_keys import ColumnKey


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
