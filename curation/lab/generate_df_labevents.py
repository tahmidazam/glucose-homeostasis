import numpy
import pandas as pd
import sqlalchemy

from curation.config import Config
from .plot_classification_performance import plot_classification_performance
from .plot_component_counts import plot_component_counts
from .query_d_labitems import query_d_labitems
from .query_labevents import query_labevents
from .read_loinc import read_loinc


def generate_df_labevents(
    engine: sqlalchemy.Engine,
    config: Config,
    subject_ids: tuple[numpy.int64],
    chunk_size: int,
) -> pd.DataFrame:
    df_labevents = query_labevents(
        engine=engine, subject_ids=subject_ids, chunk_size=chunk_size
    )

    df_d_labitems = query_d_labitems(engine=engine)

    df_loinc = read_loinc(config)

    df_d_labitems = pd.merge(
        left=df_d_labitems,
        right=df_loinc,
        how="left",
        left_on="loinc_code",
        right_on="LOINC_NUM",
    )

    df_labevents = pd.merge(
        left=df_labevents, right=df_d_labitems, how="left", on="itemid"
    )

    df_component_counts = df_labevents["COMPONENT"].value_counts().reset_index()

    plot_component_counts(df_component_counts)

    plot_classification_performance(df_labevents=df_labevents)

    return df_labevents
