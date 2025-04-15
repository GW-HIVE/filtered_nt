#!/bin/bash
#SBATCH --job-name=taxDB
#SBATCH --output=logs/taxDB-%j.log
#SBATCH --error=logs/taxDB-%j.err
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

# Create Taxonomy DB
[ -d "raw_data/new_taxdump" ] || mkdir -p "raw_data/new_taxdump"

cd raw_data/new_taxdump
curl -O -L 'ftp://ftp.ncbi.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.tar.gz'
tar xfz new_taxdump.tar.gz

cd $HOME
# create the taxonomy.db file
make nucleotide
# create the dead_taxonomy.db file
make dead
# create the protien_taxonomy.db file
make protein

