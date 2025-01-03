#!/bin/bash
#SBATCH --job-name=protDB
#SBATCH --output=logs/protDB-%j.log
#SBATCH --error=logs/protDB-%j.err
#SBATCH --chdir=/dfs9/evilain-lab/share/filtered_nt  #Set the working directory of the batch script
#SBATCH --partition=standard
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=48:00:00      # Allocate # of hours for the job
#SBATCH --mem=48G            # Allocate # of GB for memory
#SBATCH --mail-type=ALL      # Send email on job start, end, and failure
#SBATCH --mail-user=kingch2@hs.uci.edu
#SBATCH -A EVILAIN_LAB

HOME=$PWD

# create the protien_taxonomy.db file
make protein

