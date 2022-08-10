#!/usr/bin/env python3
"""Get Child TaxID of BlackList

    This script generates a black list of unwanted taxonomy names (scientific
    names) from names.dmp and all child taxonomy names: ['unclassified',
    'unidentified','uncultured','unspecified','unknown','phage','vector'] and
    ['environmental sample','artificial sequence','other sequence'].

    Input
    ^^^^^
    All inputs are currently hard-coded.
    - `database.txt`: provides utility parameters for main method.
    - `taxIdFile`: path for the `../blacklist-taxId.1.csv` output file.

    Output
    ^^^^^^
    All outputs are currently hard-coded.
    - The `blacklist-taxId.2.csv` is generated.

    Usage
    ^^^^^
    - python child_taxid_blacklist.py sort -u
        - Deletes duplicated records, and store them into:
        /data/projects/targetdbs/generated/blacklist-taxId.unique.csv
"""

__version__ = "7.0"
__status__ = "Dev"

import sqlite3
from sqlite3 import Error
from argparse import ArgumentParser, SUPPRESS

def usr_args():
    """User Arguments

    User supplied arguments from command line for function

    Returns
    -------
        ArgumentParser objects to be digested by subsequent functions.
    """

    parser = ArgumentParser(
        add_help=False,
        prog='child_taxid_blacklist.py',
        description="This script generates a black list of unwanted taxonomy"
            "names (scientific names) from names.dmp and all child taxonomy"
            "names: ['unclassified','unidentified','uncultured','unspecified',"
            "'unknown','phage','vector'] and ['environmental sample',"
            "'artificial sequence','other sequence'].")

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument('-d', '--database',
        help="'db.sqlite3' file. Should contain ",
        # default='./raw_date/taxdump/names.dmp'
        )


    # optional.add_argument('-b', '--blacklist',
    #     help="Output file to create. The `blacklist-taxId.1.csv` is generated"
    #     "and used as input for the `get-chiled-taxid-of-blacklist.py` script."
    #     "Default is `./data_output/blacklist-taxId.1.csv` ",
    #     default='./output_data/blacklist-taxId.1.csv')
    optional.add_argument('-v', '--version',
        action='version',
        version='%(prog)s ' + __version__)
    optional.add_argument('-h', '--help',
        action='help',
        default=SUPPRESS,
        help='show this help message and exit')

    # if len(sys.argv) <= 1:
    #     sys.argv.append('--help')

    return parser.parse_args()

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(conn)
    except Error as error:
        print(error)

    return conn

def select_all_tables(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT nodes.taxid, nodes.parent_taxid FROM nodes INNER JOIN names ON nodes.taxid = names.taxid AND nodes.parent_taxid='1';")

    rows = cur.fetchall()

    for row in rows:
        print(row)

def main():
    """Main Function"""
    options = usr_args()
    conn = create_connection(options.database)
    select_all_tables(conn)
    print('main')

if __name__ == '__main__':
    main()