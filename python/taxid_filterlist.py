#!/usr/bin/env python3
"""
Generate a taxonomy-based list names for filtering NT.

This script processes taxonomy names from a SQLite database, using either a default or 
user-specified list of terms to create a list of taxonomy IDs and associated 
information. The output is a CSV file containing these IDs and names.

Usage:
    taxid_filter.py [-d DATABASE] [-o OUTPUT] [--query-list QUERY_LIST] [-v] [-h]

Arguments:
    -d DATABASE, --database DATABASE
        Path to 'taxonomy.db', an SQLite database file containing taxonomy data.

    -o OUTPUT, --output OUTPUT
        Output CSV file for the generated list. Default is `./output_data/filter.csv`.

    -q QUERY_LIST, --query-list QUERY_LIST
        Optional path to a CSV file containing a custom list of terms to filter. 
        If not provided, a default list is used.

    -v, --version
        Show program's version number and exit.

    -h, --help
        Show this help message and exit.
"""


import sys
import sqlite3
import csv
from sqlite3 import Error
from argparse import ArgumentParser, SUPPRESS

__version__ = "9.0"
__status__ = "Production"


def usr_args():
    """Parse user-supplied arguments from the command line.

    Returns:
        argparse.Namespace: Parsed arguments for subsequent functions.
    """
    parser = ArgumentParser(
        add_help=False,
        prog='taxid_blacklist.py',
        description="Generate a taxonomy-based filter list of taxonomy names."
    )

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument('-d', '--database', required=True,
                          help="Path to the SQLite database file ('taxonomy.db').")

    optional.add_argument('-o', '--output', default='./output_data/filter.csv',
                          help="Path to output CSV file. Default: './output_data/filter.csv'.")

    optional.add_argument('-q', '--query-list', default=None,
                          help="Optional path to a custom query list file. Default list is used if not provided.")

    optional.add_argument('-v', '--version', action='version', version=f"%(prog)s {__version__}")
    optional.add_argument('-h', '--help', action='help', default=SUPPRESS, help="Show this help message and exit.")

    if len(sys.argv) <= 1:
        sys.argv.append('--help')

    return parser.parse_args()


def create_connection(db_file: str) -> sqlite3.Connection:
    """Create a connection to the SQLite database.

    Args:
        db_file (str): Path to the SQLite database file.

    Returns:
        sqlite3.Connection: Database connection object.
    """
    try:
        return sqlite3.connect(db_file)
    except Error as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)


def load_query_list(query_list: str = None) -> list:
    """Load terms from the query list or use a default list.

    Args:
        query_list (str): Path to a custom query list text file, if provided.

    Returns:
        list: List of terms for filtering.
    """
    default_terms = [
        "unclassified", "unidentified", "uncultured", "unspecified",
        "unknown", "phage", "vector", "environmental sample", "other sequence"
    ]

    if query_list:
        terms = []
        with open(query_list, 'r', encoding='utf-8') as file:
            terms = [line.strip().lower() for line in file if line.strip()]
        print(f"Custom query list loaded with {len(terms)} terms.")
        return terms

    print("Default query list loaded.")
    return default_terms


def filter_list(conn: sqlite3.Connection, output: str, terms: list):
    """Retrieve and filter taxonomy names, including child nodes, based on specified terms.

    Args:
        conn (sqlite3.Connection): Database connection object.
        output (str): Output path for the list CSV file.
        terms (list): List of terms for filtering.
        mode (str): Filter mode, either 'whitelist' or 'blacklist'.
    """

    # Set up CSV writing for filtered results
    with open(output, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["tax_id", "class_name", "tax_name"])

        cur = conn.cursor()
        query = """
            SELECT names.taxid, names.name, nodes.parent_taxid 
            FROM names 
            INNER JOIN nodes ON names.taxid = nodes.taxid
        """

        # Process each taxonomy record
        for tax_id, tax_name, parent_tax_id in cur.execute(query):
            lower_name = tax_name.lower()
            matches = [term for term in terms if term in lower_name]
            if matches:
                # Write each matching term
                writer.writerow([tax_id, ";".join(matches), tax_name])

                # Retrieve child nodes recursively if parent_tax_id is not root
                retrieve_children_iteratively(conn, writer, tax_id, ";".join(matches))


def retrieve_children_iteratively(conn: sqlite3.Connection, writer, parent_id: str, class_name: str):
    """Iteratively retrieve all child nodes for a given taxonomy ID and write to output.

    Args:
        conn (sqlite3.Connection): Database connection object.
        writer: CSV writer object to write output rows.
        parent_id (str): Parent Taxonomy ID to start the search.
        class_name (str): Class name associated with the taxonomy ID.
    """
    cur = conn.cursor()
    query = """
        SELECT names.taxid, names.name 
        FROM nodes 
        INNER JOIN names ON nodes.taxid = names.taxid 
        WHERE nodes.parent_taxid = ?
    """

    # Stack for iterative DFS traversal
    stack = [parent_id]

    while stack:
        current_id = stack.pop()
        cur.execute(query, (current_id,))

        for child_tax, tax_name in cur.fetchall():
            # Write child details to output
            writer.writerow([child_tax, class_name, tax_name])
            stack.append(child_tax) # Add child to stack for further exploration

def main():
    """Main function to execute the script's workflow."""
    options = usr_args()
    conn = create_connection(options.database)

    # Load query terms based on user input or default list
    terms = load_query_list(options.query_list)

    # Execute filtering and list generation
    filter_list(conn, options.output, terms)
    
    conn.close()
    print("Filter list generated successfully at:", options.output)


if __name__ == '__main__':
    main()