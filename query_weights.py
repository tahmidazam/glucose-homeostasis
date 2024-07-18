import pandas as pd
import sqlalchemy
from tqdm import tqdm

from column_keys import ColumnKey
from db_connection_critical_error import db_connection_critical_error
from generate_weights_sql_query import generate_weights_sql_query
from table_name import TableName


def query_weights(engine: sqlalchemy.Engine, subject_ids: tuple, chunk_size: int) -> pd.DataFrame:
    try:
        with engine.connect() as connection:
            weights_query = generate_weights_sql_query(subject_ids=subject_ids)

            df_weights_chunks: [pd.DataFrame] = pd.read_sql_query(sql=weights_query, con=connection,
                                                                  chunksize=chunk_size)
            df_weights = pd.DataFrame()

            for df_weights_chunk in tqdm(df_weights_chunks, desc=f"Querying {TableName.CHARTEVENTS.value} for weights"):
                df_weights = pd.concat([df_weights, df_weights_chunk])

            df_weights = df_weights.round({ColumnKey.HEIGHT.value: 2})

            df_weights.drop(columns=[ColumnKey.VALUE_NUMERICAL.value], inplace=True)

            df_weights.drop_duplicates(
                subset=[ColumnKey.SUBJECT_ID.value, ColumnKey.ICU_STAY_ID.value, ColumnKey.WEIGHT.value], inplace=True)

            return df_weights
    except sqlalchemy.exc.OperationalError:
        db_connection_critical_error(engine=engine)
