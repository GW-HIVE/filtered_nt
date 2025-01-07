#!/bin/bash
#SBATCH -o logfiles/bacteria_filter_nt%j.out
#SBATCH -e logfiles/bacteria_filter_nt%j.err
#SBATCH -t 24:00:00
#SBATCH -p short-384gb -n 32
#SBATCH -D /scratch/hivelab/

module load python3/3.10.11
python filtered_nt/filter_nt_new.py \
    -n /scratch/hivelab/blastdb/filteredNT_8.0/filteredNT_v8.0.fasta \
    -d filtered_nt/output_data/ \
    -o blastdb/bacteria_filteredNT_v8.0/bacteria_filteredNT_v8.0.fasta \
    -l filtered_nt/output_data/bacteria_filter.csv \
    -m whitelist \
    -s filtered_nt/output_data/bacteriaStats.tsv
