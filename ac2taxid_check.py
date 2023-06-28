#!/usr/bin/env python3
"""Accession TaxId Check

This script is the first of three scripts that checks if all seqAcs in nt file
have taxIds from nucl_gb.accession2taxid file, and the ones do not have taxIds
are checked in all other ac2taxid files.
"""

import sys
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
        help="'db.sqlite3' files. Should contain path to DB files",
        default='./output_data'
        )

    required.add_argument('-n', '--nt',
        help="Path to `nt` file.",
        default='./raw_data/nt'
        )

    optional.add_argument('-l', '--logfile',
        help="Log file file to create."
        "Default is `./logfiles/accession2taxid_log.txt` ",
        default='./logfiles/accession2taxid_log.txt')

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

    # protein_conn, dead_conn, taxonomy_conn = None, None, None
    print(db_file)

    try:
        protein_conn = sqlite3.connect(f'{db_file}/protein_taxonomy.db')
    except Error as error:
        raise error
    
    try:
        dead_conn = sqlite3.connect(f'{db_file}/dead_taxonomy.db')
    except Error as error:
        raise error

    try:
        taxonomy_conn = sqlite3.connect(f'{db_file}/taxonomy.db')
    except Error as error:
        raise error

    return protein_conn, dead_conn, taxonomy_conn

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

def check_nt(protein_conn, dead_conn, taxonomy_conn, nt, logfile):
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

    with open(logfile, 'a', encoding='utf-8') as log:
        for record in SeqIO.parse(nt, "fasta"):
            accession = record.id.split('.')[0]
            tax_result = get_taxonomy(taxonomy_conn, accession)
            if tax_result == 'not found':
                prot_result = get_taxonomy(protein_conn, accession)
                if prot_result == 'not found':
                    dead_result = get_taxonomy(dead_conn, accession)
                    if dead_result == 'not found':
                        log.write(f'{accession}\n')
                        print(f'No taxid found for: {accession}')
        log.write('\n')

def main():
    """Main Function"""

    options = usr_args()
    protein_conn, dead_conn, taxonomy_conn = create_connection(options.database)
    check_nt(protein_conn, dead_conn, taxonomy_conn, options.nt, options.logfile)


if __name__ == '__main__':
    main()
