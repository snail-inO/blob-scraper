#!/usr/bin/env python3

import os

import pandas as pd

def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

def filter_empties(data, column):
    data = data[data[column].notna()]
    return data

def get_file_list(path):
    return [(os.path.join(path, file), file) for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]



if __name__ == '__main__':
    data_path = 'data/transactions/'
    dst_path = 'data/blob_transactions/'
    
    files = get_file_list(data_path)
    blob_tx_ct = 0
    for i, (path, file) in enumerate(files):
        data = load_data(path)
        blob_tx = filter_empties(data, 'blob_versioned_hashes')
        blob_tx_ct += len(blob_tx)
        blob_tx.to_csv(os.path.join(dst_path, file), index=False)
        if i % 100 == 0:
            print(f'Processed {i}/{len(files)} files')
    print(f'Total Blob transactions: {blob_tx_ct}')