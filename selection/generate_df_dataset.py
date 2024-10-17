from pathlib import Path

import pandas as pd
from tqdm import tqdm

from selection.process_stay import process_stay


def generate_df_dataset(
    df_glucose_insulin: pd.DataFrame,
    df_demographics: pd.DataFrame,
    df_labevents: pd.DataFrame,
    df_prescriptions: pd.DataFrame,
    identifier_columns: list[str],
    glucose_columns: list[str],
    insulin_columns: list[str],
    demographics_columns: list[str],
    prescriptions_columns: list[str],
    rule: str,
):
    path_df_dataset = Path("./../df_cache/df_dataset")

    if path_df_dataset.is_file():
        df_dataset = pd.read_feather(path_df_dataset)

        return df_dataset

    df_dataset = df_glucose_insulin[
        identifier_columns + glucose_columns + insulin_columns
    ]

    df_dataset = pd.merge(
        left=df_dataset,
        right=df_demographics[identifier_columns + demographics_columns],
        on=identifier_columns,
        how="left",
    )

    df_labevents["loinc_summary"] = (
        df_labevents["COMPONENT"] + " " + df_labevents["SYSTEM"]
    )

    df_dataset = df_dataset.rename(columns={"timer": "charttime"})

    df_dataset["charttime"] = pd.to_datetime(
        df_dataset["charttime"], errors="coerce", utc=True
    )

    df_dataset = df_dataset.sort_values(by=["charttime"])

    tqdm.pandas()

    df_dataset = df_dataset.groupby(
        ["subject_id", "hadm_id", "icustay_id"]
    ).progress_apply(
        lambda df: process_stay(
            df_glucose_insulin=df,
            df_prescriptions=df_prescriptions,
            df_labevents=df_labevents,
            prescriptions_columns=prescriptions_columns,
            rule=rule,
        ),
        include_groups=False,
    )

    df_dataset.dropna(axis=1, how="all", inplace=True)
    df_dataset.to_feather(path_df_dataset)

    return df_dataset
