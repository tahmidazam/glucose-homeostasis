import pandas as pd
from dateutil.relativedelta import relativedelta

from curation.demographics.column_keys import ColumnKey


def calculate_age(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the age of each patient in the dataframe and adds a new age column to the dataframe.
    :param df: The dataframe from which to calculate age.
    :return: The dataframe with the age column added.
    """

    # Calculate the age of each patient into a new column.
    df[ColumnKey.AGE.value] = df.apply(
        lambda row: relativedelta(
            row[ColumnKey.IN_TIME.value],
            row[ColumnKey.DATE_OF_BIRTH.value]
        ).years,
        axis=1
    )

    return df
