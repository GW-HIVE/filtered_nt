#!/bin/bash
#SBATCH --job-name=gunzipNT
#SBATCH --output=logs/gunzipNT-%j.log
#SBATCH --error=logs/gunzipNT-%j.err
#SBATCH --chdir=/dfs9/evilain-lab/share/filtered_nt  #Set the working directory of the batch script
#SBATCH --partition=standard
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=48:00:00      # Allocate # of hours for the job
#SBATCH --mem=48G            # Allocate # of GB for memory
#SBATCH --mail-type=ALL      # Send email on job start, end, and failure
#SBATCH --mail-user=kingch2@hs.uci.edu
#SBATCH -A EVILAIN_LAB

-d output_data/ -n raw_data/nt -l logs/accession2taxid_log.txt