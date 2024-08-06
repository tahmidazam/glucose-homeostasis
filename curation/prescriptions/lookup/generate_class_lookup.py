import logging

import pandas as pd
from tqdm import tqdm

from curation.get_cache_path import get_cache_path
from curation.prescriptions.lookup.classify_drug import classify_drug


def generate_class_lookup(s_rxcui: pd.Series) -> pd.DataFrame:
    cache_filename: str = 'df_class_lookup'
    path = get_cache_path(cache_filename)

    if path.is_file():
        logging.info(f"Loaded {cache_filename} from cache")
        return pd.read_feather(path=path)

    df_class_lookup = pd.DataFrame()

    # N.B. Int64 type enables null values.
    df_class_lookup['rxcui'] = s_rxcui.drop_duplicates().dropna().astype('Int64')
    tqdm.pandas(desc='Classifying RxCUIs using RxClass and saving to cache')
    df_class_lookup = df_class_lookup.progress_apply(classify_drug, axis=1)
    df_class_lookup.to_feather(path=path)

    return df_class_lookup
