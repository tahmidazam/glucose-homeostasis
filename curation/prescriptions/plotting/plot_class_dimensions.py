import logging
from pathlib import Path

import pandas as pd
from matplotlib import pyplot as plt

from curation.prescriptions.plotting.class_types import CLASS_TYPES


def plot_class_dimensions(df_prescriptions: pd.DataFrame):
    title: str = "dimension_count_by_class_type"
    counts: tuple[tuple[str, float], ...] = ()

    for class_type in CLASS_TYPES:
        id_column_key = f"rxclass_{class_type}_name"
        count = len(df_prescriptions[id_column_key].dropna().unique())
        counts += ((class_type, count),)

    counts = tuple(sorted(counts, key=lambda x: x[1], reverse=True))

    labels, values = zip(*counts)
    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, values, color='blue')

    plt.xlabel('class type')
    plt.ylabel('number of dimensions of representative one-hot vector')
    plt.title('Dimension count by class type')

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.5, round(yval, 2), ha='center', va='bottom')

    path = Path(f"./../docs/plots/{title}.png")

    plt.savefig(path)

    logging.info(f"Saved '{title}' plot to {path}")
