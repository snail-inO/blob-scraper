#!/usr/bin/env python3

import pandas as pd

from tx_filter import load_data, get_file_list


def load_blob_txs(data_path):
    files = get_file_list(data_path)
    blob_txs = []
    for path, file in files:
        data = load_data(path)
        blob_txs.append(data)
    return pd.concat(blob_txs)


def count_dup_fields(data, column):
    return data[column].value_counts()


def fill_empty_blocks(df):
    new_indices = range(19426587, 19977246)
    df = df.reindex(new_indices, fill_value=0)
    return df.sort_index(ascending=True)


def get_sender_rank(blob_txs, stat_path):
    blob_sender_ct = count_dup_fields(blob_txs, "from_address")
    blob_sender_ct.to_csv(f"{stat_path}blob_sender_ct.csv")
    blob_sender_ct.to_json(f"{stat_path}blob_senders.json")


def get_receiver_rank(blob_txs, stat_path):
    blob_receiver_ct = count_dup_fields(blob_txs, "to_address")
    blob_receiver_ct.to_csv(f"{stat_path}blob_receiver_ct.csv")
    blob_receiver_ct.to_json(f"{stat_path}blob_receivers.json")


def get_block_tx_ct(blob_txs, stat_path):
    block_txs_ct = count_dup_fields(blob_txs, "block_number")
    block_txs_ct = fill_empty_blocks(block_txs_ct)
    block_txs_ct.to_csv(f"{stat_path}block_txs_ct.csv")


def get_tx_blob_ct(tx):
    blob_hashes = tx["blob_versioned_hashes"]
    return pd.Series(
        [
            tx["hash"],
            tx["block_number"],
            tx["from_address"],
            len(blob_hashes.split(",")),
        ]
    )

def get_sender_blob_ct(blob_txs, stat_path):
    sender_blob_sum = blob_txs.groupby("from_address")["count"].sum()
    sender_blob_sum.sort_values(ascending=False, inplace=True)
    sender_blob_sum.to_csv(f"{stat_path}blob_sender_ct.csv")

def get_block_blob_ct(blob_txs, stat_path):
    block_blob_ct = blob_txs.apply(get_tx_blob_ct, axis=1)
    block_blob_ct.columns = ["tx_hash", "block_number", "from_address", "count"]
    block_blob_ct.to_csv(f"{stat_path}tx_blob_ct.csv", index=False)

    block_blob_sum = block_blob_ct.groupby("block_number")["count"].sum()

    block_blob_sum = fill_empty_blocks(block_blob_sum)
    block_blob_sum.to_csv(f"{stat_path}block_blob_ct.csv")


if __name__ == "__main__":
    data_path = "data/blob_transactions/"
    stat_path = "data/stats/"

    # blob_txs = load_blob_txs(data_path)
    # blob_txs.to_csv(f"{stat_path}blob_txs.csv")
    blob_txs = pd.read_csv(f"{stat_path}tx_blob_ct.csv")
    print(f"Loaded {blob_txs.shape} blob txs")
    get_sender_blob_ct(blob_txs, stat_path)