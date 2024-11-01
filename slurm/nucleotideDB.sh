#!/bin/bash
#SBATCH -o output_data/nuc%j.out
#SBATCH -e output_data/nuc%j.err
#SBATCH -t 2:00:00
#SBATCH -p tiny
#SBATCH -D /scratch/hivelab/filtered_nt

module load sqlite
make nucleotide
