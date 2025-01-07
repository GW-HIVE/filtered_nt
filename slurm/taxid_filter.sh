#!/bin/bash
#SBATCH --job-name=taxFilter
#SBATCH --output=logs/taxFilter-%j.log
#SBATCH --error=logs/taxFilter-%j.err
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

echo "[$(date)] Generating nt filter list"
python python/taxid_filterlist.py -d output_data/taxonomy.db -o output_data/filter_v8.0.1.csv

echo "[$(date)] Sorting filter_v8.0.1.csv"
sort -u output_data/filter_v8.0.1.csv > output_data/filter_v8.0.1_unique.csv
