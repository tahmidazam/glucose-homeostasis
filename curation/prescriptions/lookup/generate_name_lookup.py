import logging

import pandas as pd
from tqdm import tqdm

from curation.constants import ColumnKey
from curation.get_cache_path import get_cache_path
from .identify_drug_using_approximate_match import identify_drug_using_approximate_match


def generate_name_lookup(s_drug: pd.Series, column_key: ColumnKey) -> pd.DataFrame:
    cache_filename: str = f"df_{column_key.value.lower()}_lookup"
    path = get_cache_path(cache_filename)

    if path.is_file():
        logging.info(f"Loaded {cache_filename} from cache")
        return pd.read_feather(path=path)

    df_lookup = pd.DataFrame()
    df_lookup[column_key.value] = s_drug.drop_duplicates().dropna().astype(str)
    tqdm.pandas(desc=f"Finding RxCUI from column '{column_key.value}' using RxNorm and saving to cache")
    df_lookup = df_lookup.progress_apply(identify_drug_using_approximate_match, args=[column_key], axis=1)
    df_lookup.to_feather(path=path)

    return df_lookup
