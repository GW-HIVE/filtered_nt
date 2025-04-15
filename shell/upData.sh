#!/bin/bash

# Curl for Uniprot proteoms
# Need to provide a text file with a list of UP accessions

set -Eeuo pipefail

case $# in
    1)
        up_accessions="$1"
        ;;
    *) echo "Usage: $(basename $0) up_accessions is required" >&1; exit 1;;
esac

echo [ >> output_data/results.json

for i in $(cat $up_accessions )
do
    # curl -o output_data/${i}.json `https://rest.uniprot.org/proteomes/${i}.json`
	 var1='https://rest.uniprot.org/proteomes/'
	 var2=$i'.json'
	 var3=$var1$var2
	 curl -sS $var3 >> output_data/results.json
     echo , >> output_data/results.json
done
echo {}] >> output_data/results.json