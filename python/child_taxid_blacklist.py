#!/usr/bin/env python3
"""
Generate a blacklist of unwanted taxonomy names based on specified criteria.

This script processes taxonomic identifiers and names from a SQLite database,
filtering unwanted taxonomy names (e.g., 'unclassified', 'uncultured', 'unknown').
It then outputs a blacklist CSV of taxonomic IDs, class names, and scientific names.

Usage:
    child_taxid_blacklist.py [-d DATABASE] [-b BLACKLIST] [-o OUTPUT] [-v] [-h]

Arguments:
    -d DATABASE, --database DATABASE
        Path to 'db.sqlite3', an SQLite file containing taxonomic data (required).

    -b BLACKLIST, --blacklist BLACKLIST
        Input CSV file containing taxonomy IDs and class names to filter.
        Default is `./output_data/blacklist-taxId.1.csv`.

    -o OUTPUT, --output OUTPUT
        Output CSV file for the generated blacklist.
        Default is `./output_data/blacklist_children.csv`.

    -v, --version
        Show the program's version number and exit.

    -h, --help
        Show this help message and exit.
"""

__version__ = "8.0"
__status__ = "BETA"

import sys
import csv
import sqlite3
from sqlite3 import Error
from argparse import ArgumentParser, SUPPRESS
from typing import Optional


def usr_args():
    """Parse user-supplied arguments from the command line.

    Returns:
        Namespace: Parsed arguments for subsequent functions.
    """
    parser = ArgumentParser(
        add_help=False,
        prog='child_taxid_blacklist.py',
        description="Generate a blacklist of unwanted taxonomy names and all their child nodes."
    )

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument('-d', '--database', required=True,
                          help="Path to the SQLite database file ('taxonomy.db').")

    optional.add_argument('-b', '--blacklist', default='./output_data/blacklist-taxId.1.csv',
                          help="Path to input blacklist CSV file. Default: './output_data/blacklist-taxId.1.csv'.")

    optional.add_argument('-o', '--output', default='./output_data/blacklist_children.csv',
                          help="Path to output CSV file. Default: './output_data/blacklist_children.csv'.")

    optional.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    optional.add_argument('-h', '--help', action='help', default=SUPPRESS, help='Show this help message and exit')

    if len(sys.argv) <= 1:
        sys.argv.append('--help')

    return parser.parse_args()


def create_connection(db_file: str) -> Optional[sqlite3.Connection]:
    """Create a connection to the SQLite database.

    Args:
        db_file (str): Path to the SQLite database file.

    Returns:
        sqlite3.Connection: Database connection object, or None if connection fails.
    """
    try:
        return sqlite3.connect(db_file)
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None


def get_lineage(conn: sqlite3.Connection, writer, tax_id: str, class_name: str):
    """Recursively retrieve all child nodes for a given taxonomy ID.

    Args:
        conn (sqlite3.Connection): Database connection object.
        writer: CSV writer object to write output rows.
        tax_id (str): Taxonomy ID to query.
        class_name (str): Class name associated with the taxonomy ID.
    """
    cur = conn.cursor()
    query = (
        "SELECT names.taxid, names.name FROM nodes "
        "INNER JOIN names ON nodes.taxid = names.taxid "
        "WHERE nodes.parent_taxid = ?"
    )

    cur.execute(query, (tax_id,))
    rows = cur.fetchall()

    for child_tax, tax_name in rows:
        writer.writerow([child_tax, class_name, tax_name])
        if child_tax != '1':  # avoid infinite recursion with root node
            get_lineage(conn, writer, child_tax, class_name)


def write_lineage(blacklist: str, output: str, conn: sqlite3.Connection):
    """Process the blacklist file and write results to the output file.

    Args:
        blacklist (str): Path to input blacklist file.
        output (str): Path to output file for writing results.
        conn (sqlite3.Connection): Database connection object.
    """
    with open(blacklist, 'r', encoding='utf-8') as reader_file, \
         open(output, 'w', encoding='utf-8', newline='') as output_file:

        csv_reader = csv.reader(reader_file)
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(["tax_id", "class_name", "tax_name"])

        for row in csv_reader:
            tax_id, class_name = row[0], row[1]
            get_lineage(conn, csv_writer, tax_id, class_name)


def main():
    """Main function to execute the script's workflow."""
    options = usr_args()
    conn = create_connection(options.database)

    if conn is None:
        print("Failed to establish database connection. Exiting.")
        sys.exit(1)

    write_lineage(options.blacklist, options.output, conn)
    conn.close()
    print("Blacklist generated successfully.")


if __name__ == '__main__':
    main()
