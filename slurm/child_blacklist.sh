#!/bin/bash
#SBATCH -o logfiles/c_blacklist%j.out
#SBATCH -e logfiles/c_blacklist%j.err
#SBATCH -t 2:00:00
#SBATCH -p tiny
#SBATCH -D /scratch/hivelab/filtered_nt

module load python3/3.10.11
python child_taxid_blacklist.py -d output_data/taxonomy.db