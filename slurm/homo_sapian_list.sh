#!/bin/bash
#SBATCH -o logfiles/lst_homo%j.out
#SBATCH -e logfiles/lst_homo%j.err
#SBATCH -t 24:00:00
#SBATCH -p short-384gb -n 32
#SBATCH -D /scratch/hivelab/
#SBATCH --job-name=lst_homo

module load python3/3.10.11

# Filter nucleotide sequences based on a whitelist or blacklist of taxonomy IDs.
python filtered_nt/python/taxid_filterlist.py \
        # Path to 'taxonomy.db', an SQLite database file containing taxonomy data.
    -d filtered_nt/output_data

        # Output CSV file for the generated list. Default is `./output_data/filter.csv`.
    -o filtered_nt/output_data/homo_sapian_filter.csv

        # Optional path to a CSV file containing a custom list of terms to filter. 
    -q filtered_nt/raw_data/homo_sapians.txt
