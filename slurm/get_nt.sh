#!/bin/bash
#SBATCH --job-name=get_nt
#SBATCH --output=logs/get_nt-%j.log
#SBATCH --error=logs/get_nt-%j.err
#SBATCH --chdir=/dfs9/evilain-lab/share/filtered_nt  #Set the working directory of the batch script
#SBATCH --partition=standard
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --time=48:00:00      # Allocate # of hours for the job
#SBATCH --mem=48G            # Allocate # of GB for memory
#SBATCH --mail-type=ALL      # Send email on job start, end, and failure
#SBATCH --mail-user=kingch2@hs.uci.edu
#SBATCH -A EVILAIN_LAB


    # Get NT
wget --quiet -O raw_data/nt.fasta.gz ftp://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nt.gz

    # Get NT.md5
wget --quiet -O raw_data/nt.fasta.gz ftp://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nt.gz.md5

