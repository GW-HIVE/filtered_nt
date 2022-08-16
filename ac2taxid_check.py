#!/usr/bin/env python3
"""Accession TaxId Check

This script is the first of three scripts that checks if all seqAcs in nt file
have taxIds from nucl_gb.accession2taxid file, and the ones do not have taxIds
are checked in all other ac2taxid files.


"""

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
    conn: sqlite3 db connection
        Database connection object or None
    """

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as error:
        print(error)

    return conn

def get_taxonomy(conn, accession):
    """Get Taxonomy

    Using the supplied taxonomy DB this function will check that there is a
    taxonomy ID for the associated accession.

    Parameters
    ----------
    conn: sqlite3 db connection
        Database connection object or None
    accession: str
        NCBI accession as string

    Returns
    -------
    row: tup
        A tuple object containing the accession and the taxonomy id OR a string
        indicating nothing was found in the DB.
    """

    cursor = conn.cursor()
    query = ("select * from accession_taxid where accession = ?")
    cursor.execute(query, (accession,))
    row = cursor.fetchone()
    if row is None:
        return 'not found'

    return row

def check_nt(conn, nt, logfile):
    """Chcek NT

    Parameters
    ----------
    conn: sqlite3 db connection
        Database connection object or None
    nt: str
        File path to the version of nt to be checked. 

    Results
    -------
    """

    for record in SeqIO.parse(nt, "fasta"):
        accession = record.id
        # accession = accession.split('.')[0]
        result = get_taxonomy(conn, accession)
        if result == 'not found':
            with open(logfile, 'a', encoding='utf-8') as logfile:
                logfile.write(f'{accession}\n')
            print(f'No taxid found for: {accession}')

def main():
    """Main Function"""

    options = usr_args()
    conn = create_connection(options.database)
    check_nt(conn, options.nt, options.logfile)


if __name__ == '__main__':
    main()
