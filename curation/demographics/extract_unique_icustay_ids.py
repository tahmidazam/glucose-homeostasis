import pandas as pd

from curation.constants.column_keys import ColumnKey


def extract_unique_icu_stay_ids(df_glucose_insulin: pd.DataFrame, max_identifier_count: int) -> [int]:
    """
    Extracts unique ICU stay identifiers from the glucose insulin dataset dataframe.
    :param max_identifier_count: The maximum number of unique ICU stay identifiers.
    :param df_glucose_insulin: The glucose insulin dataset dataframe.
    :return: A list of unique ICU stay identifiers.
    """
    ids: [int] = tuple(df_glucose_insulin[ColumnKey.ICU_STAY_ID.value].unique())

    if max_identifier_count > 0:
        return ids[:max_identifier_count]

    return ids
