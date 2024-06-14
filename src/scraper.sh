#!/bin/bash

set -exu

source .env

dst_dir="data"
# dst_dir="test_data"
# start=19426587
start=19684887
end=19977245
step=100

for ((i=start; i<=end; i+=step)); do
    next=$((i+step-1))
    if ((next>end)); then
        next=$end
    fi
    echo $i-$next
    ethereumetl export_blocks_and_transactions \
        -s $i \
        -e $next \
        -p $RPC_URL_QUICKNODE \
        --blocks-output "${dst_dir}/blocks/blocks_${i}-${next}.csv" \
        --transactions-output "${dst_dir}/transactions/transactions_${i}-${next}.csv"
    # sleep 10
done
