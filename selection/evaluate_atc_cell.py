import numpy as np
import pandas as pd

from selection.evaluate_whether_intervals_overlap import (
    evaluate_whether_intervals_overlap,
)


def evaluate_atc_cell(
    start: pd.Timestamp,
    df_filtered_prescription_sample: pd.DataFrame,
    rule: str,
):
    end = start + pd.Timedelta(rule)

    for sample in df_filtered_prescription_sample.iterrows():
        prescription_start = sample[1]["startdate"]
        prescription_end = sample[1]["enddate"]

        if evaluate_whether_intervals_overlap(
            start,
            end,
            prescription_start,
            prescription_end,
        ):
            return 1

    return np.nan
