#!/bin/bash
#SBATCH -o logfiles/index_virusesNT%j.out
#SBATCH -e logfiles/index_virusesNT%j.err
#SBATCH -J index_vfilNT
#SBATCH -t 1:00:00
#SBATCH -p short-384gb -n 32
#SBATCH -D /scratch/hivelab/

# indexing command for blast db w/o `parse_seqids` flag, which seems to cause memory fail.
module load blast+
makeblastdb -in /scratch/hivelab/blastdb/viruses_filteredNT_v8.0/viruses_filteredNT_v8.0.fasta \
    -dbtype nucl -out /scratch/hivelab/blastdb/viruses_filteredNT_v8.0/indexed_viruses_filteredNT_v8.0
