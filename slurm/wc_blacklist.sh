#!/bin/bash
#SBATCH -o logfiles/wc_blacklist%j.out
#SBATCH -e logfiles/wc_blacklist%j.err
#SBATCH -t 20:00
#SBATCH -p tiny
#SBATCH -D /scratch/hivelab/filtered_nt

wc -l output_data/blacklist_children_unique.csv
wc -l output_data/blacklist_children.csv 