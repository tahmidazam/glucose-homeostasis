import numpy
import pandas as pd
from matplotlib import pyplot as plt

from curation.constants import ColumnKey


def plot_glucose_trace(
    df_glucose_insulin: pd.DataFrame,
    icu_stay_id: numpy.int64,
    window_size: int = 10,
    resample_rule: pd.DateOffset | pd.Timedelta | str = "4h",
):
    sample = df_glucose_insulin[
        df_glucose_insulin[ColumnKey.ICU_STAY_ID.value] == icu_stay_id
    ]

    sample = sample.dropna(subset=["glc"])

    # Convert 'glctimer' to datetime and handle errors
    sample["glctimer"] = pd.to_datetime(sample["glctimer"], errors="coerce")

    # Drop rows where 'glctimer' couldn't be converted (NaT values)
    sample = sample.dropna(subset=["glctimer"])

    # Resample data to a 2-hour frequency and calculate mean
    sample = sample.resample(rule=resample_rule, on="glctimer").mean(numeric_only=True)

    sample["rolling_mean"] = sample["glc"].rolling(window=window_size).mean()

    plt.figure(figsize=(10, 6))
    plt.plot(sample.index, sample["glc"], color="#e5e5ea")
    plt.plot(
        sample.index,
        sample["rolling_mean"],
        label=f"{window_size}-point rolling average",
        color="red",
    )

    plt.axhline(y=70, linestyle="-", color="#34c759", label="Hypoglycemia threshold")
    plt.axhline(y=140, linestyle="-", color="#22d3ee", label="Hyperglycemia threshold")

    plt.xlabel("time")
    plt.ylabel("glucose (mg/dL)")
    plt.title("Glucose trace for ICU stay identifier 213668")
    plt.legend()
    plt.grid(True)

    plt.show()

    return
