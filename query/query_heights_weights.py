import logging
from pathlib import Path

import numpy
import pandas as pd
import sqlalchemy

from constants.column_keys import ColumnKey
from query_heights import query_heights
from query_weights import query_weights


def query_heights_weights(engine: sqlalchemy.Engine, subject_ids: tuple[numpy.int64, ...],
                          chunk_size: int) -> pd.DataFrame:
    df_heights_weights_cache = Path("df-cache/df_heights_weights.csv")

    if df_heights_weights_cache.is_file():
        df_heights_weights = pd.read_csv(df_heights_weights_cache)

        logging.info(f"Loaded df_heights_weights from cache ({df_heights_weights_cache}).")

        return df_heights_weights

    logging.info(
        f"No cached df_heights_weights found, querying database and caching to {df_heights_weights_cache}.")

    df_weights: pd.DataFrame = query_weights(engine=engine, subject_ids=subject_ids, chunk_size=chunk_size)
    df_heights: pd.DataFrame = query_heights(engine=engine, subject_ids=subject_ids, chunk_size=chunk_size)

    df_heights_weights: pd.DataFrame = pd.merge(df_heights, df_weights, on=[ColumnKey.SUBJECT_ID.value,
                                                                            ColumnKey.ICU_STAY_ID.value], how='inner')

    df_heights_weights.to_csv(df_heights_weights_cache)

    return df_heights_weights
