import logging
from pathlib import Path

import pandas as pd
from matplotlib import pyplot as plt


def plot_classification_performance(df_labevents: pd.DataFrame):
    title: str = "labevent_classification_performance"
    path = Path(f"./../docs/plots/{title}.png")

    if path.is_file():
        logging.info(f"Skipped plotting {title}, already exists")
        return

    len_df_prescriptions = len(df_labevents)
    proportions: tuple[tuple[str, float], ...] = ()

    for column_key in [
        "COMPONENT",
        "PROPERTY",
        "TIME_ASPCT",
        "SYSTEM",
        "SCALE_TYP",
        "METHOD_TYP",
        "CLASS",
    ]:
        proportion = round(
            len(df_labevents[column_key].dropna()) / len_df_prescriptions * 100, 2
        )
        proportions += ((column_key, proportion),)

    proportions = tuple(sorted(proportions, key=lambda x: x[1], reverse=True))

    labels, values = zip(*proportions)
    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, values)

    plt.xlabel("class type")
    plt.ylabel("proportion of prescription records with non-null class ids (%)")
    plt.title("Lab event classification performance")

    plt.ylim(0, 110)

    for bar in bars:
        yval = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            yval + 0.5,
            round(yval, 2),
            ha="center",
            va="bottom",
        )

    plt.savefig(path)
    logging.info(f"Saved '{title}' plot to {path}")
