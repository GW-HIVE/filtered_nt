# Filtered NT v7.0 Release Notes

************************************************************************
## Files Downloaded 

### 1. `nt` file downloaded on 2023-05-16 

ftp://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/

Name  | Last modified    | Size
------|------------------|------
nt.gz | 2023-05-16 18:01 | 277  G
nt    | 2023-05-16 12:01 | 1.06 T
filteredNT | 
    
	93,245,213 	sequences


### 2. `new_taxdump` downloaded on 2023-05-16 
   ftp://ftp.ncbi.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.tar.gz

	125 M	new_taxdump.tar.gz

file size | file name            | lines
----------|----------------------|-------
19 M      | citations.dmp        | 57,135
4.3 M     | delnodes.dmp         | 469,891
452	      | division.dmp         | 12
34 K      | excludedfromtype.dmp | 483
673 M     | fullnamelineage.dmp  | 2,511,766
4.9 K     | gencode.dmp          | 28
5.6 M     | host.dmp             | 207,017
667 K     | images.dmp           | 4,562
1.3 M     | merged.dmp           | 72,443
207 M     | names.dmp            | 3,614,948
226 M     | nodes.dmp            | 2,511,766
312 M     | rankedlineage.dmp    | 2,511,766
285 M     | taxidlineage.dmp     | 2,511,766
24 M      | typematerial.dmp     | 381,647
3.0 K     | typeoftype.dmp       | 38
   .      | total                | 14,855,268

### 3. `ac2taxid` downloaded on 2023-05-16
   ftp://ftp.ncbi.nih.gov/pub/taxonomy/accession2taxid/

records	      | file name                         | file size (compressed)
--------------|-----------------------------------|------------------------
107,821,989	  | dead_wgs.accession2taxid.gz       | 749 M
39,408,003	  | dead_nucl.accession2taxid.gz      | 282 M
146,110,304   | dead_prot.accession2taxid.gz      | 1.1 G
330,564	      | nucl_wgs.accession2taxid.EXTRA.gz | 1.6 M
656,650,780	  | nucl_wgs.accession2taxid.gz       | 4.5 G
315,533,471	  | nucl_gb.accession2taxid.gz        | 2.2 G
802,469	      | pdb.accession2taxid.gz            | 5.4 M
5,242,814,608 | prot.accession2taxid.gz           | 13  G

************************************************************************
## Database Statistics 

Database            | file size  | records in accession_taxid
--------------------|------------|----------------------------
protein_taxonomy.db | 365 G      | 5,242,861,403
taxonomy.db         | 65 G       | 972,514,757
dead_taxonomy.db    | 20 G       | 293,340,296

************************************************************************
## Filter statistics

Number of taxonomy ids that are in black list is 1,452,016.
Number of blacklisted sequences is 11,283,515 sequences.

Sequences from a given black list of sources were removed. This list
of sources, number of associated taxonomic IDs and number 
of removed sequences is given below.

blackListTaxonomyName | taxids | removed sequences
----------------------|--------|-------------------
unidentified          |  .     |  .
total                 | 1,452,016 | 11,283,515


The number of sequences in this filtered-nt release is 
	81,961,699
