import logging

import pandas as pd
from tqdm import tqdm

from curation.get_cache_path import get_cache_path
from .identify_drug_using_ndc import identify_drug_using_ndc


def generate_ndc_lookup(s_ndc: pd.Series) -> pd.DataFrame:
    cache_filename: str = 'df_ndc_lookup'
    path = get_cache_path(cache_filename)

    if path.is_file():
        logging.info(f"Loaded {cache_filename} from cache")
        return pd.read_feather(path=path)

    df_ndc_lookup = pd.DataFrame()

    # Add the NDCs to the classification lookup dataframe, removing duplicates and NaN values.
    df_ndc_lookup['ndc'] = s_ndc.drop_duplicates().dropna().astype(str)

    # Remove the '0' from the classification lookup dataframe.
    df_ndc_lookup = df_ndc_lookup[df_ndc_lookup['ndc'] != '0']

    # Use RxNorm and RxClass to classify the drugs from the NDC.
    tqdm.pandas(desc='Finding RxCUI from NDC using RxNorm and saving to cache')
    df_ndc_lookup = df_ndc_lookup.progress_apply(identify_drug_using_ndc, axis=1)

    df_ndc_lookup.to_feather(path=path)

    return df_ndc_lookup
