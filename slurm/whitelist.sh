#!/bin/bash
#SBATCH -o logfiles/whitelistViruses%j.out
#SBATCH -e logfiles/whitelistViruses%j.err
#SBATCH -t 2:00:00
#SBATCH -p tiny
#SBATCH -D /scratch/hivelab/filtered_nt

module load python3/3.10.11
python taxid_filterlist.py -d output_data/taxonomy.db -q raw_data/viruses.txt -o output_data/viruses_filter.csv