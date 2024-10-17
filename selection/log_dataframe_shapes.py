import logging
import pandas as pd
from tabulate import tabulate


def log_dataframe_shapes(
    df_demographics: pd.DataFrame,
    df_prescriptions: pd.DataFrame,
    df_labitems: pd.DataFrame,
):
    logging.info(
        "\n"
        + tabulate(
            tabular_data=[
                ["df_demographics", df_demographics.shape],
                ["df_prescriptions", df_prescriptions.shape],
                ["df_labitems", df_labitems.shape],
            ],
            headers=["dataframe", "shape"],
        )
    )
