import logging
from pathlib import Path

import numpy
import pandas as pd
import sqlalchemy
from tqdm import tqdm

from constants.column_keys import ColumnKey
from constants.table_name import TableName
from db_connection.db_connection_critical_error import db_connection_critical_error
from query.generate_heights_weights_query import generate_heights_weights_query
from query.query_heights import query_heights
from query.query_weights import query_weights


def query_heights_weights(engine: sqlalchemy.Engine, subject_ids: tuple[numpy.int64, ...],
                          chunk_size: int) -> pd.DataFrame:
    cache = Path("df_cache/df_heights_weights.feather")

    if cache.is_file():
        df_heights_weights = pd.read_feather(cache)

        logging.info(f"Loaded df_heights_weights from cache ({cache}).")

        return df_heights_weights

    try:
        with engine.connect() as connection:
            query: str = generate_heights_weights_query(subject_ids=subject_ids)

            chunks = pd.read_sql_query(sql=query, con=connection, chunksize=chunk_size)

            df_heights_weights = pd.DataFrame()

            for chunk in tqdm(chunks,
                              desc=f"No cache found, querying {TableName.CHARTEVENTS.value} and saving to {cache}"):
                df_heights_weights = pd.concat([df_heights_weights, chunk.dropna()])

            df_heights_weights.to_feather(path=cache)

            return df_heights_weights
    except sqlalchemy.exc.OperationalError:
        db_connection_critical_error(engine=engine)
