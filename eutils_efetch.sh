#!/bin/bash

# EFetch for NCBI Accessions
# Need to provide a text file with a list of NCBI accessions

set -Eeuo pipefail

case $# in
    1)
        ncbi_accessions="$1"
        ;;
    *) echo "Usage: $(basename $0) ncbi_accessions is required" >&1; exit 1;;
esac

for i in $(cat $ncbi_accessions )
do
    # echo "Fetching $i"
    (efetch -db nuccore -id $i -format fasta) >> output_data/slim_fetch.fasta
done