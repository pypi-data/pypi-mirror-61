#!/usr/bin/env bash

#
if [[ $# != 2 ]]; then
    echo "script called without name of remote conda environment!"
fi
eval $(conda shell.bash hook)
conda activate $1
spawn_adaptable_dask_cluster -m $2

