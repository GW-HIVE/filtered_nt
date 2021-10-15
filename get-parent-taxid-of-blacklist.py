"""
This script generates a black list of unwanted taxonomy names (scientific names) from names.dmp
and all child taxonomy names: [‘unclassified’,’unidentified’,’uncultured’,’unspecified’,’unknown’,
’phage’,’vector’] and [‘environmental sample’,’artificial sequence’,’other sequence’].

Input
^^^^^
All inputs are currently hard-coded.
- `nameFile`: path for the `../names.dmp` file.
- `taxIdFile`: path for the `../blacklist-taxId.1.csv` output file.

Output
^^^^^^
All outputs are currently hard-coded.
- The `blacklist-taxId.1.csv` is generated and used as input for the `get-chiled-taxid-of-blacklist.py`
script.

Usage
^^^^^
- python get-parent-taxid-of-blacklist.py sort -u
	- Deletes duplicated records, and store them into: /data/projects/targetdbs/generated/blacklist-taxId.unique.csv
"""

import os,sys
import string
from optparse import OptionParser
from Bio import Entrez, SeqIO
import glob
import MySQLdb
import util


__version__="1.0"
__status__ = "Dev"


###############################
def main():


	nameFile = "/data/projects/targetdbs/filtered-nt/downloads/names.dmp"
	taxIdFile = "/data/projects/targetdbs/filtered-nt/generated/blacklist-taxId.1.csv"
	rmName1 = ['unclassified','unidentified','uncultured', 'unspecified','unknown','phage','vector']
	rmName2 = ['environmental sample','other sequence']


	seqId = {}
	reviewId = {}
	FR = open(nameFile, "r")
	FW = open(taxIdFile, "w")
	for line1 in FR:
		deter = False
		line = line1.strip().split("|")
		featureType = line[3].strip()
		featureName1 = line[1].lower().strip().split()
		featureName2 = line[1].lower().strip()
		className = ''
		for j in rmName2:
                        if featureName2.find(j) >= 0 and line1.lower().find('scientific name') >= 0:
                                deter = True
                                className += j + ';'
		for i in rmName1:
			if i in featureName1 and line1.lower().find('scientific name') >= 0:
				deter = True
				className += i + ';'
		if deter:
			FW.write(line[0].strip() + ',' + className[:-1] + ',' + line[1].strip() + '\n')

	FR.close()
	#FW.close()


if __name__ == '__main__':
        main()

