import logging
from pathlib import Path

import pandas as pd
from matplotlib import pyplot as plt


def plot_component_counts(df_component_counts: pd.DataFrame, truncate_by: int = 30):
    title: str = "labevent_component_counts"
    path = Path(f"./../docs/plots/{title}.png")

    if path.is_file():
        logging.info(f"Skipped plotting {title}, already exists")
        return

    df_truncated_component_counts = df_component_counts.head(truncate_by)

    plt.figure(
        figsize=(
            10,
            round(
                8 * truncate_by / 30,
            ),
        )
    )
    plt.barh(
        df_truncated_component_counts[df_truncated_component_counts.columns[0]],
        df_truncated_component_counts["count"],
    )

    plt.xlabel("count")
    plt.ylabel("component")
    plt.title(f"Top {truncate_by} of {len(df_component_counts)} lab component counts")

    plt.gca().invert_yaxis()
    plt.tight_layout()

    plt.savefig(path)

    logging.info(f"Saved '{title}' plot to {path}")
