import argparse

import numpy
import numpy as np
import pandas as pd
from sqlalchemy import Engine

from curation.constants.column_keys import ColumnKey
from curation.constants.table_name import TableName
from curation.demographics.calculate_age import calculate_age
from curation.demographics.filter import Filter
from curation.demographics.is_neoplasm_or_pregnancy import is_neoplasm_or_pregnancy
from curation.demographics.query_heights_weights import query_heights_weights
from curation.demographics.query_table import query_table
from curation.plot_count_history import plot_count_history


def generate_df_demographics(
        engine: Engine,
        df_glucose_insulin: pd.DataFrame,
        subject_ids: tuple[np.int64, ...],
        main_argument_namespace: argparse.Namespace,
        icu_stay_ids: [numpy.int64]
) -> pd.DataFrame:
    """
    Generate the demographics dataframe from the MIMIC-III database. Refer to [_Curation_](../docs/demographics.md) for
    detailed documentation.
    :param main_argument_namespace: The namespace containing the command-line arguments.
    :param icu_stay_ids: The ICU stay identifiers to include.
    :param engine: The SQLAlchemy engine to use to connect to the MIMIC-III database.
    :param df_glucose_insulin: The glucose insulin dataset.
    :param subject_ids: The subject identifiers to include.
    :param chunk_size: The chunk size to use when querying the table.
    :return:
    """
    df_admissions: pd.DataFrame = query_table(
        engine=engine,
        table_name=TableName.ADMISSIONS,
        id_column_key=ColumnKey.SUBJECT_ID,
        ids=subject_ids,
        chunk_size=main_argument_namespace.chunk_size,
    )

    df_patients: pd.DataFrame = query_table(
        engine=engine,
        table_name=TableName.PATIENTS,
        id_column_key=ColumnKey.SUBJECT_ID,
        ids=subject_ids,
        chunk_size=main_argument_namespace.chunk_size,
    )

    df_icu_stays: pd.DataFrame = query_table(
        engine=engine,
        table_name=TableName.ICUSTAYS,
        id_column_key=ColumnKey.ICU_STAY_ID,
        ids=icu_stay_ids,
        chunk_size=main_argument_namespace.chunk_size,
    )

    df_diagnoses_icd: pd.DataFrame = query_table(
        engine=engine,
        table_name=TableName.DIAGNOSES_ICD,
        id_column_key=ColumnKey.SUBJECT_ID,
        ids=subject_ids,
        chunk_size=main_argument_namespace.chunk_size,
    )

    # Generate the demographics dataframe from merging tables.
    df_demographics: pd.DataFrame = pd.merge(
        left=pd.merge(
            left=df_icu_stays,
            right=df_admissions,
            on=[
                ColumnKey.HOSPITAL_ADMISSION_ID.value,
                ColumnKey.SUBJECT_ID.value
            ],
            how='inner'
        ),
        right=df_patients,
        on=ColumnKey.SUBJECT_ID.value,
        how='inner'
    )

    # Initialise the data structure to record the length of the demographics dataframe after each operation.
    demographics_len_history: tuple[tuple[str, int], ...] = ()
    demographics_len_history += (("initial", len(df_demographics)),)

    # Calculate the age of the patients.
    df_demographics: pd.DataFrame = calculate_age(df_demographics)

    # Merge the demographics dataset with the ICU stay and subject identifiers from the glucose insulin dataset to
    # respect readmission.
    df_demographics = pd.merge(
        left=df_demographics,
        right=df_glucose_insulin[[ColumnKey.ICU_STAY_ID.value, ColumnKey.FIRST_ICU_STAY.value]],
        on=ColumnKey.ICU_STAY_ID.value, how='inner'
    ).drop_duplicates()

    demographics_len_history += (("merge:glucose insulin dataset", len(df_demographics)),)

    # Filter the demographics dataframe by age.
    df_demographics: pd.DataFrame = df_demographics[
        (df_demographics[ColumnKey.AGE.value] > Filter.AGE_LOWER_BOUND.value) &
        (df_demographics[ColumnKey.AGE.value] < Filter.AGE_UPPER_BOUND.value)
        ]

    demographics_len_history += (
        (f"filter:age, a ({Filter.AGE_LOWER_BOUND.value}y < a < {Filter.AGE_UPPER_BOUND.value}y)",
         len(df_demographics)),)

    # Filter the demographics dataframe by length of stay.
    df_demographics: pd.DataFrame = df_demographics[
        (df_demographics[ColumnKey.LENGTH_OF_STAY.value] > Filter.LENGTH_OF_STAY_LOWER_BOUND.value) & (
                df_demographics[ColumnKey.LENGTH_OF_STAY.value] < Filter.LENGTH_OF_STAY_UPPER_BOUND.value)]

    demographics_len_history += ((
                                     f"filter:length of stay, l ({Filter.LENGTH_OF_STAY_LOWER_BOUND.value}d < l < {Filter.LENGTH_OF_STAY_UPPER_BOUND.value}d)",
                                     len(df_demographics)),)

    # Remove patients with diagnoses in ICD9 chapters involving neoplasms (i.e., cancer) or pregnancy.
    df_diagnoses_icd.dropna(subset=[ColumnKey.ICD9_CODE.value], inplace=True)

    non_neoplasm_or_pregnancy_related_hospital_admission_ids = df_diagnoses_icd[
        (df_diagnoses_icd[ColumnKey.SEQ_NUM.value] == 1) &
        (~df_diagnoses_icd[ColumnKey.ICD9_CODE.value].apply(is_neoplasm_or_pregnancy))
        ][ColumnKey.HOSPITAL_ADMISSION_ID.value]

    df_demographics = df_demographics[df_demographics[ColumnKey.HOSPITAL_ADMISSION_ID.value].isin(
        non_neoplasm_or_pregnancy_related_hospital_admission_ids)]

    demographics_len_history += (("filter:ICD-9 chapter", len(df_demographics)),)

    # Preserve relevant columns.
    relevant_columns: [ColumnKey] = [
        ColumnKey.SUBJECT_ID,
        ColumnKey.HOSPITAL_ADMISSION_ID,
        ColumnKey.ICU_STAY_ID,
        ColumnKey.IN_TIME,
        ColumnKey.DIAGNOSIS,
        ColumnKey.AGE,
        ColumnKey.GENDER,
    ]

    df_demographics = df_demographics[[k.value for k in relevant_columns]]

    # Query the heights and weights of the patients.
    df_heights_weights = query_heights_weights(
        engine=engine,
        subject_ids=subject_ids,
        chunk_size=main_argument_namespace.chunk_size
    )

    # Convert the chart time to a datetime type.
    df_heights_weights[ColumnKey.CHART_TIME.value] = pd.to_datetime(
        df_heights_weights[ColumnKey.CHART_TIME.value])

    # Forward- and back-fill weights and heights.
    df_heights_weights[ColumnKey.HEIGHT.value] = df_heights_weights.groupby(ColumnKey.ICU_STAY_ID.value)[
        ColumnKey.HEIGHT.value].ffill().bfill()

    df_heights_weights[ColumnKey.WEIGHT.value] = df_heights_weights.groupby(ColumnKey.ICU_STAY_ID.value)[
        ColumnKey.WEIGHT.value].ffill().bfill()

    # Take the last (i.e., most recent) height and weight for each ICU stay.
    df_heights_weights = df_heights_weights.groupby(ColumnKey.ICU_STAY_ID.value).last().reset_index()

    df_demographics = pd.merge(left=df_demographics, right=df_heights_weights,
                               on=[ColumnKey.ICU_STAY_ID.value],
                               how='left')

    demographics_len_history += (("merge:heights and weights", len(df_demographics)),)

    # Drop rows with missing height or weight.
    df_demographics.dropna(subset=[ColumnKey.HEIGHT.value, ColumnKey.WEIGHT.value], inplace=True)

    demographics_len_history += (("dropna: height | weight", len(df_demographics)),)

    # Filter the demographics dataframe by height and weight.
    df_demographics = df_demographics[df_demographics[ColumnKey.HEIGHT.value] < Filter.HEIGHT_UPPER_BOUND.value]
    df_demographics = df_demographics[df_demographics[ColumnKey.WEIGHT.value] < Filter.WEIGHT_UPPER_BOUND.value]

    demographics_len_history += (
        (f"filter:heights (< {Filter.HEIGHT_UPPER_BOUND.value}m), weights (< {Filter.WEIGHT_UPPER_BOUND.value}kg)",
         len(df_demographics)),)

    # Log the demographics length history.
    plot_count_history(count_history=demographics_len_history, title="Demographics record count", upper_x_lim=16000,
                       left=0.4)

    return df_demographics
