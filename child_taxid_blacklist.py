#!/usr/bin/env python3
"""Get Child TaxID of BlackList

usage: child_taxid_blacklist.py [-d DATABASE] [-b BLACKLIST] [-o OUTPUT] [-v]
[-h]

This script generates a black list of unwanted taxonomynames (scientific names)
from names.dmp and all child taxonomynames:['unclassified','unidentified',
'uncultured','unspecified','unknown','phage','vector'] and ['environmental
sample','artificial sequence','other sequence'].

required arguments:
  -d DATABASE, --database DATABASE
                        'db.sqlite3' file. Should contain

optional arguments:
  -b BLACKLIST, --blacklist BLACKLIST
                        Input file to use. The `blacklist-taxId.1.csv` is
                        generatedand used as input for the 
                        `child_taxid_blacklist.py` script. Default is 
                        `./data_output/blacklist-taxId.1.csv`
  -o OUTPUT, --output OUTPUT
                        Output file to create.Default is 
                        `./output_data/blacklist_children.csv`
  -v, --version         show program's version number and exit
  -h, --help            show this help message and exit
"""

__version__ = "7.0"
__status__ = "Dev"

import sys
import csv
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

    optional.add_argument('-b', '--blacklist',
        help="Input file to use. The `blacklist-taxId.1.csv` is generated"
        "and used as input for the `child_taxid_blacklist.py` script. "
        "Default is `./data_output/blacklist-taxId.1.csv` ",
        default='./output_data/blacklist-taxId.1.csv')

    optional.add_argument('-o', '--output',
        help="Output file to create."
        "Default is `./output_data/blacklist_children.csv` ",
        default='./output_data/blacklist_children.csv')

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
        Database connection object or None
    """

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as error:
        print(error)

    return conn

def get_lineage(conn, writer, tax_id=None, class_name=None):
    """Get Lineage

    Using an NCBI taxonomic identifier returns any child node with class
    name. The resulting rows are written to the output file via the supplied
    file object.

    Parameters
    ----------
    conn: sqlite3.Connection
        Database connection object

    writer:
        Python file object to write results to.

    tax_id: str
        NCBI taxonomy id for query.

    class_name:
        Class name for NCBI taxonomic node in query.

    """

    cur = conn.cursor()
    query = (
        "SELECT names.taxid, names.name FROM nodes INNER JOIN names ON " \
        "nodes.taxid WHERE nodes.taxid = names.taxid AND nodes.parent_taxid" \
        f"={tax_id};"
    )
    print(query)
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        child_tax = row[0]
        tax_name = row[1]
        writer.write(f"{child_tax}, {class_name}, {tax_name}\n")
        if child_tax != 1:
            get_lineage(conn, writer, tax_id=child_tax, class_name=class_name)

def write_lineage(blacklist, output, conn):
    """Write Lineage

    This function creates the file objects to handle writing rusults to file. 

    Parameters
    ----------
    blacklist: str
        File path for the input blacklist (input file)
    output:
        File path for the output blacklist (output file)
    conn:
        Database conncection created for the taxonomy database
        
    """
    count = 0

    with open(blacklist, 'r', encoding='utf-8') as reader:
        csvreader = csv.reader(reader)
        with open(output, 'a', encoding='utf-8') as writer:
            writer.write("tax_id, class_name, tax_name")
            for row in csvreader:
                tax_id = row[0]
                class_name = row[1]
                get_lineage(conn, writer, tax_id, class_name)

def main():
    """Main Function"""

    options = usr_args()
    blacklist = options.blacklist # 'output_data/blacklist-taxId.1.csv'
    output = options.output
    conn = create_connection(options.database)
    write_lineage(blacklist, output, conn)

if __name__ == '__main__':
    main()
