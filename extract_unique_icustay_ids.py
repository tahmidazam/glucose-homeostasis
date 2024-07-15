import pandas as pd
import logging

from column_keys import ICUSTAY_ID_COLUMN_KEY


def extract_unique_icustay_ids(df_glucose_insulin: pd.DataFrame) -> [str]:
    ids: [str] = tuple(df_glucose_insulin[ICUSTAY_ID_COLUMN_KEY].unique())

    logging.info(f"Successfully extracted {str(len(ids))} unique ICU stay identifiers.")

    return ids
