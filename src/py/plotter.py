#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def autopct_generator(limit):
    def inner_autopct(pct):
        return ("%1.1f%%" % pct) if pct > limit else ""

    return inner_autopct


def top_n(df, n, column_name):
    sorted_df = df.sort_values(by=column_name, ascending=False)
    if len(sorted_df) > n:
        top_n_df = sorted_df.iloc[:n]
        other_sum = sorted_df.iloc[n:][column_name].sum()
        other_df = pd.DataFrame({column_name: [other_sum]}, index=["Other"])
        top_n_df = pd.concat([top_n_df, other_df])
        return top_n_df
    return sorted_df


def draw_blocks_prop(data, size, path):
    print(data.median())
    data["original_index"] = data.index
    groups = np.arange(len(data)) // size

    # Calculate the mean of 'count' within each group
    data_avg = data.groupby(groups)[field].median()

    # Use the first 'original_index' value in each group as the new index
    data_avg.index = data.groupby(groups)["original_index"].first()

    fig, ax = plt.subplots()
    ax.plot(data_avg.index, data_avg.values)

    # Generate five evenly spaced indices within the range of the original data
    indices = np.linspace(0, len(data) - 1, 5).astype(int)

    # Use these indices to get the corresponding x-ticks and labels from the original data
    xticks = data.index[indices]

    ax.set_xticks(xticks)
    ax.set_xticklabels(xticks)

    ax.set_xlabel("Block number")
    ax.set_ylabel("Blob count")
    ax.set_title("Median blobs/block per 7200 blocks (1 day)")

    plt.tight_layout()
    plt.savefig(path)


def draw_sender_distribution(data, field, fig_path, fig_file):
    addr_user_path = data_path + "addr_user.csv"

    total_count = data[field].sum()
    data = top_n(data, 10, field)
    addr_user = pd.read_csv(addr_user_path, index_col=0)
    new_labels = data.index.map(addr_user["user"])

    colors = [
        "#1f77b4",  # muted blue
        "#ff7f0e",  # safety orange
        "#2ca02c",  # cooked asparagus green
        "#d62728",  # brick red
        "#9467bd",  # muted purple
        "#8c564b",  # chestnut brown
        "#e377c2",  # raspberry yogurt pink
        "#7f7f7f",  # middle gray
        "#bcbd22",  # curry yellow-green
        "#17becf",  # blue-teal
        "#aec7e8",
    ]  # light blue

    # Ensure there are enough colors for the data points
    if len(data) > len(colors):
        print(
            "Warning: Not enough distinct colors for each segment. Consider adding more colors."
        )

    fig_size = (13, 6)
    fig, ax = plt.subplots(figsize=fig_size)
    wedges, texts, autotexts = ax.pie(
        data[field], labels=None, autopct="%1.1f%%", colors=colors, radius=1.2
    )
    # data.plot(kind='pie', y=field, labels=None, autopct='%1.1f%%', ax=ax, ylabel='', colors=colors)

    # Adjust the position of the percentage text for small slices
    threshold = 10  # Threshold in percent
    for i, (wedge, text) in enumerate(zip(wedges, autotexts)):
        if wedge.theta2 - wedge.theta1 < threshold:
            x, y = text.get_position()
            new_x = 1.85 * x  # Adjust this factor as needed to move text further out
            new_y = 1.85 * y  # Adjust this factor as needed to move text further out
            text.set_position((new_x, new_y))

    ax.legend(labels=new_labels, title="", loc="center left", bbox_to_anchor=(1, 0.5))
    ax.set_title(f"Total blobs: {total_count}")

    plt.tight_layout()
    plt.savefig(fig_path + fig_file)


if __name__ == "__main__":
    fn = "block_blob_ct"
    field = "count"

    data_path = "data/stats/"
    data_file = fn + ".csv"

    fig_path = "figs/"
    fig_file = fn + "_mid" + ".png"

    size = 7200

    data = pd.read_csv(data_path + data_file, index_col=0)
    print(data.head())

    draw_blocks_prop(data, size, fig_path + fig_file)
    # draw_sender_distribution(data, field, fig_path, fig_file)