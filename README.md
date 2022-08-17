# Filtered NCBI-nt in FASTA format

Filtered NT dataset is generated by excluding sequences from the whole
nt file provided by NCBI, based on whether they have unwanted taxonomy 
names or any child taxonomy name of these unwanted ones. These unwanted 
taxonomy names are listed in the black list generated by two steps: 
(1) Getting all taxonomy names which contain the strings listed 
below (Step 3); (2) Getting all possible child taxonomy names of each 
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

# Summary of the protocol

## Step 1. Clone this repo

Choose a location for the project. You will need over 500 GB of storage for just the downloads.

`git clone https://github.com/GW-HIVE/filtered_nt.git`

## Step 2. Create a project folder

Create a new directory at the same level as the `filtered_nt` (github code) directory. You should name it something unique (mybe include the date) so that you can revisit the raw files if needed. 

```shell
> $ mkdir filtered_nt_27_07_2022
> $ ll
drwxrwxr-x. 5 username grpname           87 Jul 27 16:06 filtered_nt_27_07_2022
drwxrwxr-x. 4 username grpname         4096 Jul 29 11:14 filtered_nt_git
```

## Step 3. Download and uncompress the whole nt file

At the time of this writing the `nt.gz` was 197G and the uncompressed `nt` file expanded to 791G. The download took about an hour and a half and uncompressing it took about two and a half hours. *USE CARE!* 

- Navigate to the project folder and create two more directories: `output_data` and `raw_data`
- Navigate to `raw_data`
- Download NT:

    downloaded from: ftp://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/

    version: 2022-07-25

    command:
```
    wget ftp://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nt.gz
    gunzip nt.gz (10,473,799,628 rows)
```

## Step 4. Download and uncompress the accession2taxid files

- Create a new directory: `accession2taxid/`
- Navigate to `accession2taxid/`

The files in this directory will provide a mapping between the accession.version from
a nucleotide, protein, WGS or TSA sequence record and a taxonomy ID (taxid) from
the NCBI Taxonomy database (http://www.ncbi.nlm.nih.gov/taxonomy/).

downloaded from: ftp://ftp.ncbi.nih.gov/pub/taxonomy/

version: 2022-07-28

command:
```
	wget ftp://ftp.ncbi.nih.gov/pub/taxonomy/accession2taxid/*.gz
	gunzip *.gz
```
## Step 5. Download and uncompress the taxdump files

- Create a new directory: `taxdump/`
- Navigate to `taxdump/`

```
	wget ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz
	gunzip taxdump.tar.gz |tar -xvf
```

## Step 5. Creating a database from NCBI taxonomy data

This step is taken from https://github.com/acorg/ncbi-taxonomy-database

- Navigate to the top level of this project
- Clone the `ncbi-taxonomy-database` repo:

```
git clone https://github.com/acorg/ncbi-taxonomy-database.git
```

Your project folder should look like this now:

```shell
> $ ll
drwxrwxr-x. 2 username grpname   10 Jul 27 14:26 output_data
drwxrwxr-x. 5 username grpname 4096 Jul 27 16:53 ncbi-taxonomy-database
drwxrwxr-x. 4 username grpname   90 Jul 27 17:00 raw_data
```

- Copy the requisite files into the `ncbi-taxonomy-database` repo:

```
cp raw_data/taxdump/*.dmp ncbi-taxonomy-database/data/.
cp raw_data/accession2taxid/nucl_gb.accession2taxid.gz ncbi-taxonomy-database/data/.
```

- Navigate in to the `ncbi-taxonomy-database` directory and run `make`

```
cd ncbi-taxonomy-database/
make
```

This will create you a (currently 20GB) Sqlite3 database file, taxonomy.db, and take about 20 minutes. 

## Step 6. Generate black list

protocol: unwanted taxonomy names (scientific names) from names.dmp and all child taxonomy names of them, include:

- 'unclassified'
- 'unidentified'
- 'uncultured'
- 'unspecified'
- 'unknown'
- 'phage'
- 'vector'
- 'environmental sample'
- 'artificial sequence'
- 'other sequence'

There are three steps for generating the black list: 
1. get all taxonomy names with the strings above
2. get all child taxonomy names of them.
3. combine the two files and remove duplicates

### 6.1 get all taxonomy names with the strings above

- Navigate to the top level of the project. 
- Run the `parent_taxid_blacklist.py` script. Default values are provided but you can specify other values if needed. 

```
python3 filtered_nt/parent_taxid_blacklist.py \
    -n raw_date/taxdump/names.dmp \
    -b output_data/blacklist-taxId.1.csv
```

This will generate a file `output_data/blacklist-taxId.1.csv` that will have 11,7927 lines and be 5.4M

### 6.2 get all child taxonomy names from blacklist-taxId.1.csv

- Navigate to the top level of the project. 
- Run the `child_taxid_blacklist.py` script. Default values are provided but you can specify other values if needed. 

```
python3 git_filtered_nt/child_taxid_blacklist.py \
    -d ncbi-taxonomy-database/taxonomy.db \
    -b output_data/blacklist-taxId.1.csv
```

This will generate a file `output_data/blacklist_children.csv` that will have 1,417,479 lines and be 58M

### 6.3 combine the two files and remove duplicates

After generating `output_data/blacklist_children.csv` use the command line 
"sort -u" to delete duplicated records, and store them in
`output_data/blacklist_unique.csv`

``` shell
    sort -u output_data/blacklist-taxId.1.csv output_data/blacklist_children.csv > output_data/blacklist_unique.csv
```

This will create a new file that is 1,530,156 lines and 74M

## Step 7. Check the completion of taxonomy list (QC)

For this step you will check if all sequences access in nt file have taxonomy ids in the taxonomy DB. It is reccomended to run this step in the background (using `nohup` and `&`) so that if you loose your connection the process will not stop.

``` shell
nohup python3 git_filtered_nt/ac2taxid_check.py \
    -d ncbi-taxonomy-database/taxonomy.db -n raw_data/nt \
    -l logs/logfile.accession2taxid.txt & 
```
For version 7 this process took 14 hours and the resulting log file contained 92,306 accessions. 

	nucl_gb.accession2taxid file, and the ones do not have taxIds
	are checked in all other ac2taxid files.
script: /projects/targetdbs/scripts/check-ac2taxid-completion-step1.py
	/projects/targetdbs/scripts/check-ac2taxid-completion-step2.py
	/projects/targetdbs/scripts/check-ac2taxid-completion-step3.py
output: /data/projects/targetdbs/generated/logfile.step1.txt
	/data/projects/targetdbs/generated/logfile.step2.txt
	/data/projects/targetdbs/generated/logfile.step3.txt

This step needs a lot of memory. Suggest to run on large machine. 
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
