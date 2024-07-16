import logging
import numpy
import pandas as pd
import sqlalchemy
from tqdm import tqdm

from column_keys import SUBJECT_ID_COLUMN_KEY, HOSPITAL_ADMISSION_ID_COLUMN_KEY, ICU_STAY_ID_COLUMN_KEY


def query_table(
        engine: sqlalchemy.Engine,
        table_name: str,
        id_column_key: str,
        ids: [numpy.int64],
        chunk_size: int,
) -> pd.DataFrame:
    """
    Query a table in the MIMIC-III database, filtering by a list of identifiers.
    :param engine: The SQLAlchemy engine to use to connect to the MIMIC-III database.
    :param table_name: The name of the table to query.
    :param id_column_key: The column key to filter by. Must be a column referring to an identifier.
    :param ids: The list of identifiers to form the predicate.
    :param chunk_size: The chunk size to use when querying the table.
    :return: The resulting DataFrame from the query.
    """
    allowed_filter_id_column_keys: [str] = [SUBJECT_ID_COLUMN_KEY, HOSPITAL_ADMISSION_ID_COLUMN_KEY,
                                            ICU_STAY_ID_COLUMN_KEY]

    if id_column_key not in allowed_filter_id_column_keys:
        raise ValueError(f"Argument filter_id_column_key must be in [{", ".join(allowed_filter_id_column_keys)}], "
                         f"received {id_column_key}.")

    try:
        with engine.connect() as connection:
            dfs: [pd.DataFrame] = []

            for chunk_index in tqdm(range(0, len(ids), chunk_size), desc=f"Querying '{table_name}'"):
                chunk: [int] = tuple([int(n) for n in ids[chunk_index: chunk_index + chunk_size]])

                query: str = f"""
                    SELECT *
                    FROM mimiciii.{table_name}
                    WHERE {id_column_key} IN {chunk}
                    """

                df_chunk: pd.DataFrame = pd.read_sql_query(sql=query, con=connection, params=chunk)

                dfs.append(df_chunk)

            return pd.concat(dfs)
    except sqlalchemy.exc.OperationalError:
        logging.critical(
            f"Connection to server '{engine.url.database}' failed. Ensure the server is running locally and accepting "
            f"connections on the selected socket.")
