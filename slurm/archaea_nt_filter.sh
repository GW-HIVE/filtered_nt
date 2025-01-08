#!/bin/bash
#SBATCH --job-name=ntFilter
#SBATCH --output=logs/ntFilter-%j.log
#SBATCH --error=logs/ntFilter-%j.err
#SBATCH --chdir=/dfs9/evilain-lab/share/filtered_nt  #Set the working directory of the batch script
#SBATCH --partition=standard
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=48:00:00      # Allocate # of hours for the job
#SBATCH --mem=48G            # Allocate # of GB for memory
#SBATCH --mail-type=ALL      # Send email on job start, end, and failure
#SBATCH --mail-user=kingch2@hs.uci.edu
#SBATCH -A EVILAIN_LAB

module load python3/3.10.11
python filtered_nt/filter_nt_new.py \
    -n /scratch/hivelab/blastdb/filteredNT_8.0/filteredNT_v8.0.fasta \
    -d filtered_nt/output_data/ \
    -o blastdb/archaea_filteredNT_v8.0/archaea_filteredNT_v8.0.fasta \
    -l filtered_nt/output_data/archaea_filter.csv \
    -m whitelist \
    -s filtered_nt/output_data/archaeaStats.tsv
