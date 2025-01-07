#!/bin/bash
#SBATCH -o logfiles/viruses_filter_nt%j.out
#SBATCH -e logfiles/viruses_filter_nt%j.err
#SBATCH -t 10:00:00
#SBATCH -p highMem
#SBATCH -D /scratch/hivelab/filtered_nt

module load python3/3.10.11
python filter_nt_new.py \
    -n output_data/filteredNT_v8.0.fasta \
    -d output_data/ \
    -o output_data/viruses_filteredNT_v8.0.fasta \
    -l output_data/viruses_filter.csv \
    -m whitelist \
    -s output_data/virusesStats.tsv