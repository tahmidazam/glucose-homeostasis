import logging

import pandas as pd
from tqdm import tqdm

from curation.get_cache_path import get_cache_path
from .identify_drug_using_gsn import identify_drug_using_gsn


def generate_gsn_lookup(s_gsn: pd.Series) -> pd.DataFrame:
    cache_filename: str = 'df_gsn_lookup'
    path = get_cache_path(cache_filename)

    if path.is_file():
        logging.info(f"Loaded {cache_filename} from cache")
        return pd.read_feather(path=path)

    df_gsn_lookup = pd.DataFrame()
    df_gsn_lookup['gsn'] = s_gsn.drop_duplicates().dropna().astype(str)
    tqdm.pandas(desc='Finding RxCUI from GSN using RxNorm and saving to cache')
    df_gsn_lookup = df_gsn_lookup.progress_apply(identify_drug_using_gsn, axis=1)
    df_gsn_lookup.to_feather(path=path)

    return df_gsn_lookup
