#!/bin/bash
#SBATCH --job-name=ntIndex
#SBATCH --output=logs/ntIndex-%j.log
#SBATCH --error=logs/ntIndex-%j.err
#SBATCH --chdir=/dfs9/evilain-lab/share/filtered_nt  #Set the working directory of the batch script
#SBATCH --partition=standard
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --time=48:00:00      # Allocate # of hours for the job
#SBATCH --mem=48G            # Allocate # of GB for memory
#SBATCH --mail-type=ALL      # Send email on job start, end, and failure
#SBATCH --mail-user=kingch2@hs.uci.edu
#SBATCH -A EVILAIN_LAB

/share/crsp/lab/evilain/share/bin/ncbi-blast-2.16.0+/bin/makeblastdb -in /dfs9/evilain-lab/share/blastdb/filteredNT_v8.0.1/filteredNT_v8.0.1.fasta \
    -dbtype nucl -out /dfs9/evilain-lab/share/blastdb/filteredNT_v8.0.1/indexed_filteredNT_v8.0.1

