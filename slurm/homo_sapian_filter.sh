#!/bin/bash
#SBATCH -o logfiles/human_filter_nt%j.out
#SBATCH -e logfiles/human_filter_nt%j.err
#SBATCH -t 24:00:00
#SBATCH -p short-384gb -n 32
#SBATCH -D /scratch/hivelab/
#SBATCH --job-name=fltr_homo

module load python3/3.10.11

# Filter nucleotide sequences based on a whitelist or blacklist of taxonomy IDs.
python filtered_nt/filter_nt_new.py \

    # Path to the nucleotide FASTA file.
    -n /scratch/hivelab/blastdb/filteredNT_8.0/filteredNT_v8.0.fasta \

    # Directory path to the SQLite database files.
    -d filtered_nt/output_data/ \

    # Path to output file for filtered sequences in FASTA format.
    -o blastdb/bacteria_filteredNT_v8.0/bacteria_filteredNT_v8.0.fasta \

    # Path to the CSV file containing taxonomy IDs to filter.
    -l filtered_nt/output_data/homo_filter.csv \

    # Specify 'blacklist' to filter out items or 'whitelist' to include only specified items.
    -m whitelist \

    # Path to output stats file (TSV format). Only used in blacklist mode. Default: ./output_data/blackstats.tsv
    -s filtered_nt/output_data/HomoStats.tsv
