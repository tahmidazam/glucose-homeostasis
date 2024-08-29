from pathlib import Path

import pandas as pd

from curation.config import Config


def read_loinc(config: Config):
    loinc_directory: Path = Path(
        f"./../../Loinc_{config.loinc_version}/LoincTable/Loinc.csv"
    )

    df_loinc = pd.read_csv(loinc_directory, dtype=str)

    return df_loinc
