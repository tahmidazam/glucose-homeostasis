import logging

import numpy
import pandas as pd
import sqlalchemy

from curation.config import Config
from .plot_classification_performance import plot_classification_performance
from .plot_component_counts import plot_component_counts
from .query_d_labitems import query_d_labitems
from .query_labevents import query_labevents
from .read_loinc import read_loinc
from ..get_cache_path import get_cache_path


def generate_df_labevents(
    engine: sqlalchemy.Engine,
    config: Config,
    subject_ids: tuple[numpy.int64],
    chunk_size: int,
) -> pd.DataFrame:
    cache_filename = "df_classified_labevents"
    path = get_cache_path(cache_filename)

    if path.is_file():
        logging.info(f"Loaded {cache_filename} from cache")
        return pd.read_feather(path=path)

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

    df_component_counts = (
        (df_labevents["COMPONENT"] + " (" + df_labevents["SYSTEM"] + ")")
        .value_counts()
        .reset_index()
    )

    df_component_counts.rename(columns={"index": "component (system)"})

    df_component_counts["count per subject identifier"] = df_component_counts[
        "count"
    ] / len(subject_ids)

    with open("./../docs/lab-components.md", "w") as file:
        df_component_counts.to_markdown(buf=file, index=False)

    plot_component_counts(df_component_counts, truncate_by=79)
    plot_classification_performance(df_labevents=df_labevents)

    df_labevents.to_feather(path=path)

    return df_labevents
