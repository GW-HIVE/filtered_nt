#!/bin/bash
#SBATCH -o output_data/dead%j.out
#SBATCH -e output_data/dead%j.err
#SBATCH -t 2:00:00
#SBATCH -p tiny
#SBATCH -D /scratch/hivelab/filtered_nt

module load sqlite
make dead