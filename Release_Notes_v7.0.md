# Filtered NT v7.0 Release Notes

************************************************************************
## Files Downloaded 

### 1. `nt` file downloaded on 2023-05-16 

ftp://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/

Name  | Last modified    | Size
------|------------------|------
nt.gz | 2023-05-16 18:01 | 277G
nt    | 2023-05-16 12:01 | 1.1T 
    
	14,384,694,720 	sequences


### 2. `new_taxdump` downloaded on 2023-05-16 
   ftp://ftp.ncbi.nih.gov/pub/taxonomy/new_taxdump

	2,383,434 	names
	1,601,859 	scientific names


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

Sequences from a given black list of sources were removed. This list
of sources, number of associated taxonomic IDs and number 
of removed sequences is given below.

blackListTaxonomyName | taxids | removed sequences
----------------------|--------|-------------------
unidentified          | 49     | 97
uncultured            |  1	   | 2
unknown	              | 342    | 1026
unspecified           | 68     | 11435
unclassified          | 182192 | 847187
other sequence        | 12666  | 233354
phage                 | 4594   | 8445
environmental sample  | 50697  | 6398042
unknown-manually      | 1      | 4
total                 | 250610 | 7499592


The number of sequences in this filtered-nt release is 
	34,939,806
