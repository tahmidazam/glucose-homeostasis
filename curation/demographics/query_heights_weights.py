import logging
from pathlib import Path

import numpy
import pandas as pd
import sqlalchemy
from tqdm import tqdm

from curation.demographics.db_connection_critical_error import db_connection_critical_error
from curation.demographics.generate_heights_weights_query import generate_heights_weights_query
from curation.demographics.table_name import TableName


def query_heights_weights(engine: sqlalchemy.Engine, subject_ids: tuple[numpy.int64, ...],
                          chunk_size: int) -> pd.DataFrame:
    """
    Query the heights and weights from the chart events table, caching the result.
    :param engine: The SQLAlchemy engine to use to connect to the MIMIC-III database.
    :param subject_ids: The subject identifiers to include.
    :param chunk_size: The chunk size to use when querying the table.
    :return: The resulting DataFrame from the query.
    """
    cache = Path("./../df_cache/df_heights_weights.feather")

    if cache.is_file():
        df_heights_weights = pd.read_feather(cache)

        logging.info(f"Loaded df_heights_weights from cache ({cache}).")

        return df_heights_weights

    try:
        with engine.connect() as connection:
            dfs: [pd.DataFrame] = []

            for chunk_index in tqdm(
                    range(0, len(subject_ids), chunk_size),
                    desc=f"No cache found, querying {TableName.CHARTEVENTS.value} (heights, weights) and saving to {cache}"
            ):
                subject_ids_chunk: [int] = subject_ids[chunk_index: chunk_index + chunk_size]

                query: str = generate_heights_weights_query(subject_ids=subject_ids_chunk)

                df_chunk: pd.DataFrame = pd.read_sql_query(sql=query, con=connection)
                dfs.append(df_chunk)

            df_heights_weights = pd.concat(dfs)

            df_heights_weights.to_feather(path=cache)

            return df_heights_weights
    except sqlalchemy.exc.OperationalError:
        db_connection_critical_error(engine=engine)
