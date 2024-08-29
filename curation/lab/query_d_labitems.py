import logging
from pathlib import Path

import pandas as pd
import sqlalchemy

from curation.constants import TableName
from curation.throw_db_con_critical_error import throw_db_con_critical_error


def query_d_labitems(engine: sqlalchemy.Engine) -> pd.DataFrame:
    name = "d_labitems"
    cache = Path(f"./../df_cache/{name}.feather")

    if cache.is_file():
        df = pd.read_feather(cache)

        logging.info(f"Loaded {name} from cache ({cache}).")

        return df

    try:
        with engine.connect() as connection:
            query: str = f"""
                    SELECT *
                    FROM mimiciii.{TableName.D_LABITEMS.value}
                    """

            df_prescriptions: pd.DataFrame = pd.read_sql_query(
                sql=query, con=connection
            )
            df_prescriptions.to_feather(cache)

            return df_prescriptions
    except sqlalchemy.exc.OperationalError:
        throw_db_con_critical_error(engine=engine)
