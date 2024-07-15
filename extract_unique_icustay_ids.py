import argparse

import pandas as pd
import logging

from column_keys import ICUSTAY_ID_COLUMN_KEY


def extract_unique_icustay_ids(df_glucose_insulin: pd.DataFrame, argument_namespace: argparse.Namespace) -> [str]:
    ids: [str] = tuple(df_glucose_insulin[ICUSTAY_ID_COLUMN_KEY].unique())

    logging.info(f"Successfully extracted {str(len(ids))} unique ICU stay identifiers.")

    if argument_namespace.max <= 0:
        return ids
    else:
        logging.info(f"Truncating to the first {argument_namespace.max} unique ICU stay identifiers.")
        return ids[:argument_namespace.max]


x
