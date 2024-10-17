import pandas as pd


def generate_hyperglycaemic_dataset(df_dataset: pd.DataFrame) -> pd.DataFrame:
    df_hyperglycaemic_records = df_dataset[df_dataset["glc"] > 180]

    hyperglycaemic_subject_ids = df_hyperglycaemic_records.index.get_level_values(
        "subject_id"
    ).unique()

    df_hyperglycaemic_dataset = df_dataset.loc[
        df_dataset.index.get_level_values("subject_id").isin(hyperglycaemic_subject_ids)
    ]
    df_hyperglycaemic_dataset = df_hyperglycaemic_dataset.dropna(axis=1, how="all")

    return df_hyperglycaemic_dataset
