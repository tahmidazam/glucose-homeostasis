import pandas as pd

from curation.constants import ColumnKey
from selection.evaluate_atc_cell import evaluate_atc_cell


def process_stay(
    df_glucose_insulin: pd.DataFrame,
    df_prescriptions: pd.DataFrame,
    df_labevents: pd.DataFrame,
    prescriptions_columns: list[str],
    rule: str,
):
    subject_id = df_glucose_insulin.name[0]
    hadm_id = df_glucose_insulin.name[1]
    icustay_id = df_glucose_insulin.name[2]

    df_prescriptions_sample = df_prescriptions[
        (df_prescriptions[ColumnKey.ICU_STAY_ID.value] == icustay_id)
        & (df_prescriptions[ColumnKey.HOSPITAL_ADMISSION_ID.value] == hadm_id)
        & (df_prescriptions[ColumnKey.SUBJECT_ID.value] == subject_id)
    ][prescriptions_columns].dropna()

    df_labevents_sample = df_labevents[
        (df_labevents[ColumnKey.HOSPITAL_ADMISSION_ID.value] == hadm_id)
        & (df_labevents[ColumnKey.SUBJECT_ID.value] == subject_id)
    ]

    labevents = df_labevents_sample["loinc_summary"].dropna().unique()

    df_loinc_value_pair = df_labevents_sample[
        ["charttime", "loinc_summary", "valuenum"]
    ].dropna()

    df_loinc_value_pair["charttime"] = pd.to_datetime(
        df_loinc_value_pair["charttime"], errors="coerce", utc=True
    )

    df_loinc_value_pair_pivot = df_loinc_value_pair.pivot_table(
        index="charttime",
        columns="loinc_summary",
        values="valuenum",
        aggfunc="first",  # or other aggregation function if needed
    )

    # Replace NaNs with your desired values and rename columns
    df_loinc_value_pair_pivot.columns = [
        f"loinc_{col.replace(' ', '_')}" for col in df_loinc_value_pair_pivot.columns
    ]

    df_glucose_insulin = pd.merge(
        left=df_glucose_insulin,
        right=df_loinc_value_pair_pivot,
        on="charttime",
        how="inner",
    )

    df_glucose_insulin["charttime"] = pd.to_datetime(
        df_glucose_insulin["charttime"], errors="coerce", utc=True
    )

    df_glucose_insulin = df_glucose_insulin.dropna(subset=["charttime"])

    df_glucose_insulin.set_index("charttime", inplace=True)

    df_glucose_insulin = df_glucose_insulin.resample(rule=rule).first()

    df_prescriptions_sample["atc_level_1"] = df_prescriptions_sample[
        "rxclass_ATC1-4_id"
    ].apply(lambda x: x[0])

    df_prescriptions_sample["atc_level_2"] = df_prescriptions_sample[
        "rxclass_ATC1-4_id"
    ].apply(lambda x: x[0:3])

    atc_level_2_classes = df_prescriptions_sample["atc_level_2"].unique()

    df_prescriptions_sample["startdate"] = pd.to_datetime(
        df_prescriptions_sample["startdate"], errors="coerce", utc=True
    )
    df_prescriptions_sample["endtime"] = pd.to_datetime(
        df_prescriptions_sample["enddate"], errors="coerce", utc=True
    )

    df_glucose_insulin["age"] = df_glucose_insulin["age"].ffill().bfill()
    df_glucose_insulin["gender"] = df_glucose_insulin["gender"].ffill().bfill()
    df_glucose_insulin["weight"] = df_glucose_insulin["weight"].ffill().bfill()
    df_glucose_insulin["height"] = df_glucose_insulin["height"].ffill().bfill()

    for level_2_class in atc_level_2_classes:
        df_filtered_prescription_sample = df_prescriptions_sample[
            df_prescriptions_sample["atc_level_2"] == level_2_class
        ]

        df_glucose_insulin[
            f"atc2_{level_2_class}"
        ] = df_glucose_insulin.index.to_series().apply(
            lambda start: evaluate_atc_cell(
                start=start,
                df_filtered_prescription_sample=df_filtered_prescription_sample,
                rule=rule,
            )
        )

    return df_glucose_insulin
