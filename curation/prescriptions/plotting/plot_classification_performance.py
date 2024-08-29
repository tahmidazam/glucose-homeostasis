import logging
from pathlib import Path

import pandas as pd
from matplotlib import pyplot as plt

from curation.prescriptions.plotting.class_types import CLASS_TYPES


def plot_classification_performance(df_prescriptions: pd.DataFrame):
    title: str = "classification_performance"
    len_df_prescriptions = len(df_prescriptions)
    proportions: tuple[tuple[str, float], ...] = ()

    for class_type in CLASS_TYPES:
        id_column_key = f"rxclass_{class_type}_id"
        proportion = round(len(df_prescriptions[id_column_key].dropna()) / len_df_prescriptions * 100, 2)
        proportions += ((class_type, proportion),)

    proportions = tuple(sorted(proportions, key=lambda x: x[1], reverse=True))

    labels, values = zip(*proportions)
    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, values, color='blue')

    plt.xlabel('class type')
    plt.ylabel('proportion of prescription records with non-null class ids (%)')
    plt.title('Classification performance by class type')

    plt.ylim(0, 100)

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.5, round(yval, 2), ha='center', va='bottom')

    path = Path(f"./../docs/plots/{title}.png")
    plt.savefig(path)
    logging.info(f"Saved '{title}' plot to {path}")
