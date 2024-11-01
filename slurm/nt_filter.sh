#!/bin/bash
#SBATCH -o logfiles/filter_nt%j.out
#SBATCH -e logfiles/filter_nt%j.err
#SBATCH -t 5:00:00
#SBATCH -p highMem
#SBATCH -D /scratch/hivelab/filtered_nt

module load python3/3.10.11
python filter_nt.py -n raw_data/nt -d output_data/ -o output_data/filteredNT_v8.0.fasta -b output_data/blacklist_children_unique.csv -s output_data/blackstats.tsv