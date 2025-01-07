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
echo "[$(date)] Downloading nt.fasta.gz"
wget --quiet -O raw_data/nt.gz ftp://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nt.gz

    # Get NT.md5
echo "[$(date)] Downloading nt.fasta.gz.md5"
wget --quiet -O raw_data/nt.gz.md5 ftp://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nt.gz.md5

# Verify MD5 checksum
cd raw_data
echo "[$(date)] Verifying MD5"
md5sum -c nt.gz.md5

if [ $? -eq 0 ]; then
    echo "MD5 checksum verification passed."
else
    echo "MD5 checksum verification failed!" >&2
    exit 1
fi

