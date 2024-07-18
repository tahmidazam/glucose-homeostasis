import logging
import numpy
import pandas as pd
import sqlalchemy
from tqdm import tqdm

from constants.column_keys import ColumnKey
from db_connection_critical_error import db_connection_critical_error
from constants.table_name import TableName


def query_table(
        engine: sqlalchemy.Engine,
        table_name: TableName,
        id_column_key: ColumnKey,
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
    allowed_filter_id_column_keys: [ColumnKey] = [
        ColumnKey.SUBJECT_ID,
        ColumnKey.HOSPITAL_ADMISSION_ID,
        ColumnKey.ICU_STAY_ID
    ]

    if id_column_key not in allowed_filter_id_column_keys:
        formatted_key_array: str = ", ".join([str(i.value) for i in allowed_filter_id_column_keys])

        logging.critical(
            f"Argument filter_id_column_key must be in [{formatted_key_array}], received {id_column_key}.")

    try:
        with engine.connect() as connection:
            dfs: [pd.DataFrame] = []

            for chunk_index in tqdm(range(0, len(ids), chunk_size), desc=f"Querying '{table_name.value}'"):
                chunk: [int] = tuple([int(n) for n in ids[chunk_index: chunk_index + chunk_size]])

                query: str = f"""
                    SELECT *
                    FROM mimiciii.{table_name.value}
                    WHERE {id_column_key.value} IN {chunk}
                    """

                df_chunk: pd.DataFrame = pd.read_sql_query(sql=query, con=connection)
                dfs.append(df_chunk)

            return pd.concat(dfs)
    except sqlalchemy.exc.OperationalError:
        db_connection_critical_error(engine=engine)
