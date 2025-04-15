#!/usr/bin/env python3

"""Filter NT Slim

This script further filters an existing filtered_Nt file based on a given list of accessions. 

"""
import sys
import csv
from datetime import datetime
import sqlite3
from sqlite3 import Error
from argparse import ArgumentParser, SUPPRESS
from Bio import SeqIO

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
        prog='filter-nt-slim.py',
        description="This script filters the nt files that were manually"
			"added in ac2taxids.")

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument('-n', '--nt',
        help="Path to `nt` file.",
        default='./raw_data/nt'
        )

    required.add_argument('-o', '--output',
        help="New NT file file to create."
        "Default is `./output_data/filteredNT_slim.fasta` ",
        default='./output_data/filteredNT_slim.fasta')

    required.add_argument('-l', '--list',
        help="List of desired accessions. Should contain NCBI accessions, one per line",
        default='./raw_data/slim_accessions.txt'
        )

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

def get_accessions(list_file):
    with open(list_file, 'r', encoding='utf-8') as accession_list:
        data = accession_list.read()
        accessions = data.split('\n')
    return accessions

def filter_nt(nt, output, accessions):
    """Filter NT Slim"""

    count = 0
    accession_count = len(accessions)
    with open(output, 'w', encoding='utf-8') as slim:
        for record in SeqIO.parse(nt, 'fasta'):
            accession = record.id.split('.')[0]
            if count == accession_count:
                break
            if accession in accessions:
                count += 1
                slim.write(">%s\n%s\n" % (record.id, record.seq))
                print(record.id, count, accession_count-count)

def main():
    """Main Function"""

    print('Start: ', datetime.utcnow())
    options = usr_args()
    print(options)
    accessions = get_accessions(options.list)
    filter_nt(options.nt, options.output, accessions=accessions)

if __name__ == '__main__':
    main()
