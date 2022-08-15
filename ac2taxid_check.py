#!/usr/bin/env python3
"""Accession TaxId Check

This script is the first of three scripts that checks if all seqAcs in nt file
have taxIds from nucl_gb.accession2taxid file, and the ones do not have taxIds
are checked in all other ac2taxid files.


"""

from argparse import ArgumentParser, SUPPRESS
from Bio import SeqIO
import glob
import csv


__version__="7.0"
__status__ = "Dev"

def usr_args():
    """User Arguments

    User supplied arguments from command line for function

    Returns
    -------
        ArgumentParser objects to be digested by subsequent functions.
    """

    parser = ArgumentParser(
        add_help=False,
        prog='ac2taxid_check.py',
        description="This script is the first of three scripts that checks if"
        "all seqAcs in nt file have taxIds from nucl_gb.accession2taxid file,"
        " and the ones do not have taxIds are checked in all other ac2taxid" 
        "files.")

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument('-p', '--pathlist',
        help="Path to `accession2taxid` directory. Should contain NCBI"
        "accession to taxonomy files",
        default='./output_data/accession2taxid/nucl_*.accession2taxid'
        )

    required.add_argument('-n', '--nt',
        help="Path to `nt` file.",
        default='./raw_data/nt'
        )

    optional.add_argument('-l', '--logfile',
        help="Log file file to create."
        "Default is `./output_data/blacklist_children.csv` ",
        default='./logs/logfile.accession2taxid.txt')

    optional.add_argument('-v', '--version',
        action='version',
        version='%(prog)s ' + __version__)
    optional.add_argument('-h', '--help',
        action='help',
        default=SUPPRESS,
        help='show this help message and exit')

    if len(sys.argv) <= 1:
        sys.argv.append('--help')

    return parser.parse_args()

def main():

    options = usr_args()
    print(options)
	# patList = "/data/projects/targetdbs/filtered-nt/downloads/nucl_*.accession2taxid.2017-05-21"

	# fileList = glob.glob(patList)

	# ntFile = "/data/projects/targetdbs/filtered-nt/downloads/nt.2017-05-21"

	# FW = open("/data/projects/targetdbs/filtered-nt/generated/logfile.step1.txt", "w")
	# ac2taxid = {}
	# for fileName in fileList:
	# 	if fileName.find("nucl_gb.accession2taxid") >= 0:
	# 		i = 0
	# 		with open(fileName, 'rb') as csvfile:
	# 			csvreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
	# 			for row in csvreader:
	# 				seqAc = row[0].strip()
	# 				ac2taxid[seqAc] = 1
	# 				if i%10000000 == 0:
	# 					print("Done loading ", fileName, i)
	# 				i += 1
	

	# i = 0
	# for record in SeqIO.parse(ntFile, "fasta"):
	# 	seqAc = record.id
	# 	seqAc = seqAc.split('.')[0]
	# 	if seqAc not in ac2taxid:
	# 		FW.write("No taxid found for: %s\n" % (seqAc))
	# 	if i%10000000 == 0:
	# 		print("Done parsing",  i)
	# 	i += 1

	# FW.close()


if __name__ == '__main__':
        main()

