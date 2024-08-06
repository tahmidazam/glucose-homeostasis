from matplotlib import pyplot as plt


def plot_count_history(count_history: tuple[tuple[str, int], ...], title: str, upper_x_lim: int, left=float):
    labels, values = zip(*count_history[::-1])

    plt.figure(figsize=(8, 4))

    plt.title(title)

    bars = plt.barh(labels, values, color='blue')

    plt.subplots_adjust(left=left)
    plt.xlim(0, upper_x_lim)

    for bar_index in range(len(bars)):
        bar = bars[bar_index]
        next_bar = bars[bar_index + 1] if bar_index < len(bars) - 1 else None
        if next_bar:
            plt.text(
                bar.get_width() + 0.0125 * upper_x_lim,
                bar.get_y() + bar.get_height() / 2,
                f"{int(bar.get_width())} ({int(bar.get_width() - next_bar.get_width())})",
                ha='left',
                va='center'
            )
        else:
            plt.text(
                bar.get_width() + 0.0125 * upper_x_lim,
                bar.get_y() + bar.get_height() / 2,
                f"{int(bar.get_width())} ",
                ha='left',
                va='center'
            )

    plt.savefig(f"./../docs/plots/{title.lower().replace(' ', '_')}.png")
