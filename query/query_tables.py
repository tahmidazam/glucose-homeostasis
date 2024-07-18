import numpy
import pandas as pd
import sqlalchemy

from constants.column_keys import ColumnKey
from logging_utils.log_table_query_summary import log_table_query_summary
from query.query_table import query_table
from constants.table_name import TableName


def query_tables(
        engine: sqlalchemy.Engine,
        subject_ids: [numpy.int64],
        icu_stay_ids: [numpy.int64],
        chunk_size: int
):
    df_admissions: pd.DataFrame = query_table(
        engine=engine,
        table_name=TableName.ADMISSIONS,
        id_column_key=ColumnKey.SUBJECT_ID,
        ids=subject_ids,
        chunk_size=chunk_size,
    )
    df_patients: pd.DataFrame = query_table(
        engine=engine,
        table_name=TableName.PATIENTS,
        id_column_key=ColumnKey.SUBJECT_ID,
        ids=subject_ids,
        chunk_size=chunk_size,
    )
    df_diagnoses_icd: pd.DataFrame = query_table(
        engine=engine,
        table_name=TableName.DIAGNOSES_ICD,
        id_column_key=ColumnKey.SUBJECT_ID,
        ids=subject_ids,
        chunk_size=chunk_size,
    )
    df_icu_stays: pd.DataFrame = query_table(
        engine=engine,
        table_name=TableName.ICUSTAYS,
        id_column_key=ColumnKey.ICU_STAY_ID,
        ids=icu_stay_ids,
        chunk_size=chunk_size,
    )

    log_table_query_summary(
        df_admissions=df_admissions,
        df_patients=df_patients,
        df_diagnoses_icd=df_diagnoses_icd,
        df_icu_stays=df_icu_stays
    )

    return df_admissions, df_patients, df_diagnoses_icd, df_icu_stays
