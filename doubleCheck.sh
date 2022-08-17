#!/bin/bash

# Curl for NCBI Trace to retrieve SRR analysis values
# Need to provide a text file with a list of SRR accessions
for acc in $(cat ../logs/logfile.accession2taxid_test.txt)
do
	 grep -i $acc raw_data/accession2taxid/dead_*
done