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

module load python/3.10.2

source env/bin/activate

python python/filter_nt.py \
	-n raw_data/nt \
	-d output_data/ \
	-o output_data/filteredNT_v8.0.1.fasta \
	-s output_data/blackstats.tsv \
	-l output_data/filter_v8.0.1_unique.csv \
	-m blacklist

