#!/bin/bash
#SBATCH -o logfiles/p_blacklist%j.out
#SBATCH -e logfiles/p_blacklist%j.err
#SBATCH -t 2:00:00
#SBATCH -p tiny
#SBATCH -D /scratch/hivelab/filtered_nt

module load python3/3.10.11
python parent_taxid_blacklist.py -n raw_data/new_taxdump/names.dmp