#!/bin/bash
#SBATCH -o logfiles/sort_u%j.out
#SBATCH -e logfiles/sort_u%j.err
#SBATCH -t 20:00
#SBATCH -p tiny
#SBATCH -D /scratch/hivelab/filtered_nt

sort -u output_data/blacklist_children.csv > output_data/blacklist_children_unique.csv