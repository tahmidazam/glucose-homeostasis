import logging
from pathlib import Path

import numpy
import pandas as pd
import sqlalchemy
from tqdm import tqdm

from curation.constants import TableName, ColumnKey
from curation.throw_db_con_critical_error import throw_db_con_critical_error


def query_labevents(
    engine: sqlalchemy.Engine, subject_ids: tuple[numpy.int64], chunk_size: int
) -> pd.DataFrame:
    name = "df_labevents"

    cache = Path(f"./../df_cache/{name}.feather")

    if cache.is_file():
        df = pd.read_feather(cache)

        logging.info(f"Loaded {name} from cache ({cache}).")

        return df

    try:
        with engine.connect() as connection:
            dfs: [pd.DataFrame] = []

            for chunk_index in tqdm(
                range(0, len(subject_ids), chunk_size),
                desc=f"No cache found, querying '{TableName.LABEVENTS.value}' and saving to {cache}",
            ):
                chunk: [int] = tuple(
                    [
                        int(n)
                        for n in subject_ids[chunk_index : chunk_index + chunk_size]
                    ]
                )

                query: str = f"""
                    SELECT *
                    FROM mimiciii.{TableName.LABEVENTS.value}
                    WHERE {ColumnKey.SUBJECT_ID.value} IN {chunk}
                    """

                df_chunk: pd.DataFrame = pd.read_sql_query(sql=query, con=connection)
                dfs.append(df_chunk)

            df: pd.DataFrame = pd.concat(dfs)
            df.to_feather(path=cache)

            return df
    except sqlalchemy.exc.OperationalError:
        throw_db_con_critical_error(engine=engine)
