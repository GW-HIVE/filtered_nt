#!/usr/bin/env python3
"""Accession TaxId Check

This script is the first of three scripts that checks if all seqAcs in nt file
have taxIds from nucl_gb.accession2taxid file, and the ones do not have taxIds
are checked in all other ac2taxid files.


"""

import sys
from argparse import ArgumentParser, SUPPRESS
from Bio import SeqIO
import glob
import csv
import os
import sqlite3
from sqlite3 import Error

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

    required.add_argument('-d', '--database',
        help="'db.sqlite3' file. Should contain ",
        # default='./raw_date/taxdump/names.dmp'
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

#    if len(sys.argv) <= 1:
#        sys.argv.append('--help')

    return parser.parse_args()

def create_connection(db_file):
    """Create Connection

    Creates a database connection to the SQLite database
    specified by the db_file

    Parameters
    ----------
    db_file: str
        file path to the database file to query.

    Returns
    -------
        Database connection object or None
    """

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as error:
        print(error)

    return conn

def get_taxonomy(conn, accession):
    """get the taxonomy"""

    cursor = conn.cursor()
    query = ("select * from accession_taxid where accession = ?")
    cursor.execute(query, (accession,))
    row = cursor.fetchone()
    if row is None:
        return 'not found'
    else:
        return row

def check_nt(conn, nt):
    """
    """

    for record in SeqIO.parse(nt, "fasta"):
        accession = record.id
        # accession = accession.split('.')[0]
        if get_taxonomy(conn, accession) == 'not found':
            print(f'No taxid found for: {accession}')
        else:
            print(f'GOT EM: {accession}, {get_taxonomy}')

def main():
    """Main Function"""

    options = usr_args()
    print(options)            


if __name__ == '__main__':
    main()
