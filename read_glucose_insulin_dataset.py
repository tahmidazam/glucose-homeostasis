import pandas as pd

GLUCOSE_INSULIN_REPOSITORY_DIRECTORY = (
    './../curated-data-for-describing-blood-glucose-management-in-the-intensive-care-unit-1.0.1/Datasets/')
GLUCOSE_INSULIN_PAIR_FILENAME = 'glucose_insulin_pair.csv'


def read_glucose_insulin_dataset() -> pd.DataFrame:
    """
    Reads the 'Curated Data for Describing Blood Glucose Management in the Intensive Care Unit' dataset, specifically
    the file 'glucose_insulin_pair.csv'.
    :return: A dataframe containing the dataset.
    """
    filepath = f"{GLUCOSE_INSULIN_REPOSITORY_DIRECTORY}/{GLUCOSE_INSULIN_PAIR_FILENAME}"

    df: pd.DataFrame = pd.read_csv(filepath)

    print(
        f"Successfully read {str(len(df))} entries from 'Curated Data for Describing Blood Glucose Management in the "
        f"Intensive Care Unit'.")

    return df
