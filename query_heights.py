import pandas as pd
import sqlalchemy
from tqdm import tqdm

from column_keys import ColumnKey
from db_connection_critical_error import db_connection_critical_error
from generate_heights_sql_query import generate_heights_sql_query
from table_name import TableName


def query_heights(engine: sqlalchemy.Engine, subject_ids: tuple, chunk_size: int) -> pd.DataFrame:
    try:
        with engine.connect() as connection:
            heights_query = generate_heights_sql_query(subject_ids=subject_ids)

            df_heights_chunks: [pd.DataFrame] = pd.read_sql_query(sql=heights_query, con=connection,
                                                                  chunksize=chunk_size)

            df_heights = pd.DataFrame()

            for df_heights_chunk in tqdm(df_heights_chunks, desc=f"Querying {TableName.CHARTEVENTS.value} for heights"):
                df_heights = pd.concat([df_heights, df_heights_chunk])

            df_heights = df_heights.round({ColumnKey.HEIGHT.value: 2})

            df_heights.drop(columns=[ColumnKey.VALUE_NUMERICAL.value], inplace=True)

            df_heights.drop_duplicates(
                subset=[ColumnKey.SUBJECT_ID.value, ColumnKey.ICU_STAY_ID.value, ColumnKey.HEIGHT.value], inplace=True)

            return df_heights
    except sqlalchemy.exc.OperationalError:
        db_connection_critical_error(engine=engine)
