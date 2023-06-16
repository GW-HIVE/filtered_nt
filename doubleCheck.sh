#!/bin/bash

# Takes the logfile of accessions with missing taxIds from the db.
# Greps the files in the accession2taxid dir to find missing tax ids.

# to break the if/then
output=0

for acc in $(cat logs/logfile.accession2taxid.txt)
do
    #if output is zero
    if [[ $output == 0 ]];
    then
        # grep result asinged to output
        output=$(grep -m 1 $acc raw_data/accession2taxid/*)
        # if the value for output (grep result) is NULL
        if [ -z "$output" ]
            then
            # Line for missing var in file
            output="no results for $acc"
        fi
        # stdout is sent to file
        echo $output
    fi
    output=0
done
