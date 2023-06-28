#!/bin/bash

set -Eeuo pipefail

case $# in
    2)
        nucl_gb="$1"
        dbfile="$2"
        ;;
    *) echo "Usage: $(basename $0) accession-file db-file" >&2; exit 1;;
esac

tmp=$(mktemp)
trap 'rm -f $tmp' 0 1 2 3 15
echo $nucl_gb

case $nucl_gb+'pdb.accession2taxid.gz' in
    *.gz) gunzip -c < $nucl_gb'pdb.accession2taxid.gz' | tail -n +2 | cut -f1,2 > $tmp;;
    *) tail -n +2 < $nucl_gb | cut -f1,2 > $tmp;;
esac

wc -l $tmp

case $nucl_gb+'prot.accession2taxid.gz' in
    *.gz) gunzip -c < $nucl_gb'prot.accession2taxid.gz' | tail -n +2 | cut -f1,2 >> $tmp;;
    *) tail -n +2 < $nucl_gb | cut -f1,2 >> $tmp;;
esac

wc -l $tmp

sqlite3 <<EOT
.open $dbfile
CREATE TABLE IF NOT EXISTS accession_taxid (
    accession VARCHAR UNIQUE PRIMARY KEY,
    taxid INTEGER NOT NULL
);

DROP INDEX IF EXISTS accession_taxid_accession_idx;

.mode tabs
.import $tmp accession_taxid
CREATE UNIQUE INDEX accession_taxid_accession_idx ON accession_taxid(accession);
EOT