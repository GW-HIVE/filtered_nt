# Filtered NCBI-nt in FASTA format

Filtered NT dataset is generated by excluding sequences from the whole
nt file provided by NCBI, based on whether they have unwanted taxonomy 
names or any child taxonomy name of these unwanted ones. These unwanted 
taxonomy names are listed in the black list generated by two steps:
1) Getting all taxonomy names which contain the strings listed 
below (Step 3); 
2) Getting all possible child taxonomy names of each 
of the taxonomy names from (1). For example, "other sequences" 
(taxId: 28384) is excluded with all its child taxonomy names including 
"artificial sequence", "vector", "synthetic", and so on.

We have chosen to apply the Creative Commons Attribution 3.0
Unsupported License to this version of the software.



|Version | Downloadable Files | File Size | Release Notes|NCBI Download Date|
|--------|--------------------|-----------|--------------|------------------|
|Vesrion 6.0| [Filtered NT v6.0](https://hive.biochemistry.gwu.edu/prd/filterednt//content/filtered_nt_July_2018.fasta)| 168G|[Release Notes v6](https://hive.biochemistry.gwu.edu/filterednt/releasenotesv6)|July 2018|
|Version 5.0|[Filtered_NT v5.0](https://hive.biochemistry.gwu.edu/prd//filterednt/content/Filtered_NTv5.0.fasta)|131G|[Release Notes v5.0](https://hive.biochemistry.gwu.edu/filterednt/releasenotesv5)|May 2017|
|Version 4.0| [Filtered NT v4.0](https://hive.biochemistry.gwu.edu/prd//filterednt/content/Filtered_NTv4.0.fasta)|110G|[Release Notes v4.0](https://hive.biochemistry.gwu.edu/filterednt/releasenotesv4)|July 2016|




# Summary of the protocols

************************************************************************
## Step 0. Set up the local repo
************************************************************************
Clone these repos and add data directories:

	git clone https://github.com/GW-HIVE/filtered_nt.git
	git clone https://github.com/acorg/ncbi-taxonomy-database
	cd filtered_nt
	mkdir raw_data
	mkdir output_data
	mkdir logfiles

Create and activate virtual environment:

	python -m venv env
	. env/bin/activate
	python -m pip install requirements.txt

************************************************************************
## Step 1. Download the whole nt file
************************************************************************
This is a very large file. It will take a long time.

downloaded from: ftp://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/

commands:

	cd raw_data
    wget ftp://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nt.gz
    gunzip nt.gz

************************************************************************
## Step 2. Download the taxonomy list 
************************************************************************
downloaded from: ftp://ftp.ncbi.nih.gov/pub/taxonomy/

accession2taxid version: 2023-06-19

commands:

	mkdir accession2taxid
	cd accession2taxid
	wget ftp://ftp.ncbi.nih.gov/pub/taxonomy/accession2taxid/*.gz
	gunzip *.gz

************************************************************************
## Step 3. Create Taxonomy DB 
************************************************************************
Hat tip to https://github.com/acorg/ncbi-taxonomy-database

taxdump version: 2023-06-20

commands:

	mkdir taxdump
	cd taxdump
	curl -O -L 'ftp://ftp.ncbi.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.tar.gz'
	tar xfz new_taxdump.tar.gz
	cp ../accession2taxid/nucl_gb.accession2taxid.gz .

The extra copy of `nucl_gb.accession2taxid.gz` makes it easier to build the
taxonomy DB

	cd ../../ncbi-taxonomy-database

Modify the `Makefile`:

	TAXONOMY_DIR := ../filtered_nt/raw_data/new_taxdump
	DB = taxonomy.db


************************************************************************
## Step 4. Generate black list
************************************************************************
Unwanted taxonomy names (scientific names) from names.dmp and all child
taxonomy names of them, include:

		['unclassified','unidentified','uncultured', 'unspecified','unknown',
		'phage','vector', 'environmental sample','artificial sequence',
		'other sequence']

There are two scripts for generating the black list. The first will get all taxonomy names with the strings above. The second will get all child taxonomy names of those terms above.

 - script 1: `parent_taxid_blacklist.py`
	
	default output: `./output_data/blacklist-taxId.1.csv`
	
 - script 2: `child_taxid_blacklist.py`
	
	default output: `./output_data/blacklist_children.csv`

After generating `blacklist_children.csv`, use command line "sort -u" to delete duplicated records, and store the results in a duplicate file:

	sort -u blacklist_children.csv > blacklist_children_unique.csv

QC step: Compare the newly generated file with the original version.

	wc -l blacklist_children_unique.csv
		1452016 blacklist_children_unique.csv

	wc -l blacklist_children.csv 
		1457194 blacklist_children.csv


************************************************************************
## Step 5. Check the completion of taxonomy list (QC)
************************************************************************
First check if all seqAcs in nt file have taxIds from 
nucl_gb.accession2taxid file, and the ones do not have taxIds are checked
in all other ac2taxid files.


 - script 1: `ac2taxid_check.py`

	default output: `./logfiles/accession2taxid_log.txt`
 
 - script 2:  `check-ac2taxid-completion-step2.py`

	/projects/targetdbs/scripts/check-ac2taxid-completion-step2.py
	/projects/targetdbs/scripts/check-ac2taxid-completion-step3.py

output: /data/projects/targetdbs/generated/logfile.step1.txt
	/data/projects/targetdbs/generated/logfile.step2.txt
	/data/projects/targetdbs/generated/logfile.step3.txt


        123 records of PDB accessions have extra characters, fixed 
	that in step3.py.
	However, 28 records are not in the files, search taxIds
	manually for them (/data/projects/targetdbs/generated/ \
	logfile.step3.manually.added.txt).


************************************************************************
## Step 5. Get the seqAc-taxonomy list
************************************************************************
protocol: Exclude those taxIds in the blacklist. And first get all 
	seqAc-taxIds from nucl_gb.accession2taxid, and all of other
	ac2taxid files from both version 05/21/2017 and 05/30/2017.
script: /projects/targetdbs/scripts/get-seqac2taxid.py
output: /data/projects/targetdbs/generated/logfile.ac2taxid.list.txt
QC step: All seqAcs in nt files are mapped to at least one taxId. The
	number of seqAcs in the list matches the one in nt file.
	SeqAcs with multiple taxIds are listed in:
	/data/projects/targetdbs/generated/seqAc-with-multiple-taxids.txt


************************************************************************
## Step 6. Filtering nt file
************************************************************************
protocol: Remember to add those manually added ac2taxids.
script: /projects/targetdbs/scripts/filter-nt.py
output: /data/projects/targetdbs/generated/filtered_nt_Jun06-2017.fasta
QC script: /projects/targetdbs/scripts/check-removed-seqacs-count.py
