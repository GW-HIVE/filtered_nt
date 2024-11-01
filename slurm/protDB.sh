#!/bin/bash
#SBATCH -o output_data/prot%j.out
#SBATCH -e output_data/prot%j.err
#SBATCH -t 2:00:00
#SBATCH -p tiny
#SBATCH -D /scratch/hivelab/filtered_nt

module load sqlite
make protein