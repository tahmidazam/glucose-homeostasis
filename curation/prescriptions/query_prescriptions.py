import logging
from pathlib import Path

import pandas as pd
import sqlalchemy

from curation.constants import TableName, ColumnKey
from curation.throw_db_con_critical_error import throw_db_con_critical_error


def query_prescriptions(engine: sqlalchemy.Engine) -> pd.DataFrame:
    cache = Path(f"./../df_cache/df_prescriptions.feather")

    if cache.is_file():
        df = pd.read_feather(cache)

        logging.info(f"Loaded df_prescriptions from cache ({cache}).")

        return df

    try:
        with engine.connect() as connection:
            query: str = f"""
                SELECT *
                FROM mimiciii.{TableName.PRESCRIPTIONS.value}
    	        ORDER BY {ColumnKey.DRUG.value}
                """

            df_prescriptions: pd.DataFrame = pd.read_sql_query(sql=query, con=connection)
            df_prescriptions.to_feather(cache)

            return df_prescriptions
    except sqlalchemy.exc.OperationalError:
        throw_db_con_critical_error(engine=engine)
