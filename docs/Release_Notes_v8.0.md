# Filtered NT v8.0 Release Notes

************************************************************************
## Files Downloaded 

### 1. `nt` file downloaded on 2024-10-18  

NCBI "Last modified": 2024-02-08 08:41

ftp://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/

 Name           | Last modified    | Size | sequence count |
----------------|------------------|------|----------------|
nt.gz           | 2024-02-08 08:41 | 378G |  102,960,590   |
nt              | 2024-02-08 08:41 | 1.5T |  102,960,590   |
filteredNT v8.0 | 2024-10-29 22:52 | 1.4T |   90,366,870   |


### 2. `new_taxdump` downloaded on 2024-10-18 
   ftp://ftp.ncbi.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.tar.gz

	2024-10-18  132M  	new_taxdump.tar.gz

file size | file name            | lines
----------|----------------------|-------
19 M      | citations.dmp        | 57,135
4.3 M     | delnodes.dmp         | 469,891
452	    | division.dmp         | 12
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
   .      | total                | 15,863,316

### 3. `ac2taxid` downloaded on 2023-05-16
   ftp://ftp.ncbi.nih.gov/pub/taxonomy/accession2taxid/

File size (compressed)| File name                         | RECORDS
|---------------------|-----------------------------------|----------|
|                326M | dead_nucl.accession2taxid.gz      | 66108423 |
|                1.2G | dead_prot.accession2taxid.gz      | 40051792 |
|                765M | dead_wgs.accession2taxid.gz       |    19589 |
|                2.3G | nucl_gb.accession2taxid.gz        | 12848430 |
|                 20M | nucl_wgs.accession2taxid.EXTRA.gz |    22847 |
|                4.9G | nucl_wgs.accession2taxid.gz       |  6893027 |
|                6.3M | pdb.accession2taxid.gz            |  4160591 |
|                9.2G | prot.accession2taxid.gz           |  1381969 |
|                19G  | total                             |   730178 |

************************************************************************
## Database Statistics 

Database            | file size  | records in accession_taxid
--------------------|------------|----------------------------
protein_taxonomy.db | 69 G       | 
taxonomy.db         | 49 G       | 
dead_taxonomy.db    | 21 G       | 313,706,452

************************************************************************
## Filter statistics

- Number of taxonomy ids that are in black list is 8,366,747.
- Number of blacklisted sequences is 11,517,143 sequences.

Sequences from a given black list of sources were removed. This list
of sources, number of associated taxonomic IDs and number 
of removed sequences is given below.

blackListTaxonomyName | taxids   | removed sequences
----------------------|----------|-------------------
unclassified          |1,008,451 | 3,847,745
phage                 |  12,461  | 30,826
other sequence        |  18,336  | 252,346
uncultured            |  26,141  | 7,833,628
unidentified          |  1,865   | 125,636
vector                |  16,234  | 29,410
unknown               |  350     | 2,122
unidentified;vector   |  0       | 0
environmental sample  |  51,691  | 738,1678
unspecified           |  91      | 34,087
phage;vector          |  0       | 0
uncultured;phage      |  0       | 0
uncultured            |  26,141  | 7,833,628
total                 | 1,161,761| 27,371,106  

