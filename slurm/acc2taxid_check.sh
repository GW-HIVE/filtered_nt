#!/bin/bash
#SBATCH -o logfiles/acc2taxid%j.out
#SBATCH -e logfiles/acc2taxid%j.err
#SBATCH -t 3:00:00
#SBATCH -p tiny
#SBATCH -D /scratch/hivelab/filtered_nt

module load python3/3.10.11
python ac2taxid_check.py -d output_data -n raw_data/nt