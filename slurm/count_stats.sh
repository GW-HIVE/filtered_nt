#!/bin/bash
#SBATCH -o logfiles/countStats%j.out
#SBATCH -e logfiles/countStats%j.err
#SBATCH -t 4:00:00
#SBATCH -p tiny
#SBATCH -D /scratch/hivelab/filtered_nt

grep -c ">" raw_data/nt
grep -c ">" output_data/filteredNT_v8.0.fasta
wc -l raw_data/new_taxdump/*dmp
ll -h raw_data/new_taxdump
ll -h output_data/*.db