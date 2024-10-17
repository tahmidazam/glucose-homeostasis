import pandas as pd


def evaluate_whether_intervals_overlap(
    start1: pd.Timestamp,
    end1: pd.Timestamp,
    start2: pd.Timestamp,
    end2: pd.Timestamp,
) -> bool:
    start1 = start1.tz_localize(None)
    end1 = end1.tz_localize(None)
    start2 = start2.tz_localize(None)
    end2 = end2.tz_localize(None)

    return start1 < end2 and start2 < end1
