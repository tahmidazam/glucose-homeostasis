import pandas as pd
from matplotlib import pyplot as plt


def plot_demographics_len_history(demographics_len_history: tuple[tuple[str, int], ...]):
    """
    Plot the demographics record count history.
    :param demographics_len_history: The history of the demographics record count, as a tuple of label, value pairs.
    """
    labels, values = zip(*demographics_len_history[::-1])

    plt.figure(figsize=(8, 4))

    plt.title("Demographics record count")

    bars = plt.barh(labels, values, color='blue')

    plt.subplots_adjust(left=0.4)
    plt.xlim(0, 16000)

    for bar_index in range(len(bars)):
        bar = bars[bar_index]
        next_bar = bars[bar_index + 1] if bar_index < len(bars) - 1 else None
        if next_bar:
            plt.text(
                bar.get_width() + 200,
                bar.get_y() + bar.get_height() / 2,
                f"{int(bar.get_width())} ({int(bar.get_width() - next_bar.get_width())})",
                ha='left',
                va='center'
            )
        else:
            plt.text(
                bar.get_width() + 200,
                bar.get_y() + bar.get_height() / 2,
                f"{int(bar.get_width())} ",
                ha='left',
                va='center'
            )

    plt.savefig('plots/demographics_record_count.png')
