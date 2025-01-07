#!/usr/bin/env python3

"""
Filter NT

This script filters nucleotide (nt) files based on a list of taxonomy IDs
to either include (whitelist) or exclude (blacklist) sequences. It uses 
database connections to find taxonomy IDs for each accession in the nt file 
and checks against a specified list of taxonomy IDs. It the "blacklist" mode
is specified the list file will EXCLUDE accessions in the list. If 
"whitelist" is specified then the filtering will INCLUDE ONLY the accessions
in the list.

Input
-----
User-supplied arguments specify the paths to the required files:
- `nt`: Path to the nucleotide FASTA file (e.g., ../nt.DATE).
- `database`: Path to the SQLite database files containing taxonomy information.
- `output`: Path to output file for filtered sequences in FASTA format.
- `list`: Path to a CSV file containing taxonomy IDs to use as a whitelist or blacklist.
- `mode`: Specifies whether the provided list should be used as a "blacklist" or "whitelist".

Output
------
- `output`: The filtered nucleotide sequences in FASTA format.
- `stats` (only in blacklist mode): A summary file listing filtered sequences' accessions, taxonomy IDs, and associated names.

Usage
-----
Run this script with command-line arguments:
    python filter_nt.py -n <nt file> -d <database path> -o <output file> -l <list file> -m <whitelist|blacklist> [-s <stats file>]

Example:
    python filter_nt.py -n ../nt.DATE -d ../output_data -o ./filteredNT.fasta -l ./list_unique.csv -m blacklist -s ./blackstats.tsv
"""

import sys
import csv
from datetime import datetime
import sqlite3
from sqlite3 import Error
from argparse import ArgumentParser, SUPPRESS
from Bio import SeqIO

__version__ = "8.0"
__status__ = "Prd"

def usr_args():
    """Parse and return command-line arguments for user-specified file paths.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = ArgumentParser(
        add_help=False,
        prog='filter_nt.py',
        description="Filter nucleotide sequences based on a whitelist or blacklist of taxonomy IDs."
    )

    # Argument groups for required and optional arguments
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument('-n', '--nt', required=True,
                          help="Path to the nucleotide FASTA file.")
    required.add_argument('-d', '--database', required=True,
                          help="Directory path to the SQLite database files.")
    required.add_argument('-o', '--output', required=True,
                          help="Path to output file for filtered sequences in FASTA format.")
    required.add_argument('-l', '--list', required=True,
                          help="Path to the CSV file containing taxonomy IDs to filter.")
    required.add_argument('-m', '--mode', choices=['blacklist', 'whitelist'], required=True,
                          help="Specify 'blacklist' to filter out items or 'whitelist' to include only specified items.")

    optional.add_argument('-s', '--stats', default='./output_data/blackstats.tsv',
                          help="Path to output stats file (TSV format). Only used in blacklist mode. Default: ./output_data/blackstats.tsv")
    optional.add_argument('-v', '--version', action='version', version=f"%(prog)s {__version__}")
    optional.add_argument('-h', '--help', action='help', default=SUPPRESS,
                          help="Show this help message and exit.")

    if len(sys.argv) <= 1:
        sys.argv.append('--help')

    return parser.parse_args()


def read_list(list_file: str) -> dict:
    """Load filter list data (whitelist or blacklist) into a dictionary for quick lookups.

    Args:
        list_file (str): Path to the list CSV file.

    Returns:
        dict: Dictionary mapping taxonomy IDs to their descriptions.
    """
    filter_dict = {}
    with open(list_file, 'r', encoding='utf-8') as list_file:
        reader = csv.reader(list_file)
        for row in reader:
            filter_dict[row[0]] = (row[1], row[2])
    print("Filter list loaded:", datetime.utcnow())
    return filter_dict


def create_connection(db_dir: str):
    """Establish connections to necessary SQLite databases.

    Args:
        db_dir (str): Directory containing the SQLite database files.

    Returns:
        tuple: Connections to protein, dead, and taxonomy databases, respectively.
    """
    def connect_db(db_name):
        try:
            return sqlite3.connect(f"{db_dir}/{db_name}")
        except Error as error:
            print(f"Error connecting to {db_name}: {error}")
            return None

    protein_conn = connect_db("protein_taxonomy.db")
    dead_conn = connect_db("dead_taxonomy.db")
    taxonomy_conn = connect_db("taxonomy.db")
    
    return protein_conn, dead_conn, taxonomy_conn


def get_taxonomy(conn, accession: str):
    """Retrieve taxonomy ID for a given accession from the database.

    Args:
        conn: SQLite database connection.
        accession (str): Accession to search for.

    Returns:
        tuple or str: A tuple containing the accession and taxonomy ID or 'not found'.
    """
    cursor = conn.cursor()
    query = "SELECT * FROM accession_taxid WHERE accession = ?"
    cursor.execute(query, (accession,))
    return cursor.fetchone() or 'not found'


def filter_nt(protein_conn, dead_conn, taxonomy_conn, nt_file: str, filter_dict: dict, output_file: str, stats_file: str, mode: str):
    """Filter the nucleotide sequences based on the specified mode (blacklist or whitelist).

    Args:
        protein_conn, dead_conn, taxonomy_conn: Database connections.
        nt_file (str): Path to the nucleotide FASTA file.
        filter_dict (dict): Dictionary of taxonomy IDs to filter by.
        output_file (str): Path to save filtered sequences.
        stats_file (str): Path to save filter stats, only used in blacklist mode.
        mode (str): Filter mode, either 'blacklist' or 'whitelist'.
    """
    is_blacklist = (mode == 'blacklist')
    with open(output_file, 'w', encoding='utf-8') as filtered:
        if is_blacklist:
            with open(stats_file, 'w', encoding='utf-8') as stat_file:
                writer = csv.writer(stat_file, delimiter='\t')
                writer.writerow(['accession', 'taxid', 'node', 'name'])

                for record in SeqIO.parse(nt_file, 'fasta'):
                    accession = record.id.split('.')[0]
                    result = get_taxonomy(taxonomy_conn, accession) or \
                             get_taxonomy(protein_conn, accession) or \
                             get_taxonomy(dead_conn, accession)

                    if result == 'not found':
                        print(f"{accession} Not Found")
                        continue

                    # Blacklist mode: Exclude if found in filter_dict, log to stats if excluded
                    if is_blacklist and str(result[1]) in filter_dict:
                        writer.writerow([accession, result[1], *filter_dict[str(result[1])]])
                    else:
                        filtered.write(f">{record.id}\n{record.seq}\n")
        else:
            # Whitelist mode: Include only if found in filter_dict, skip stats
            for record in SeqIO.parse(nt_file, 'fasta'):
                accession = record.id.split('.')[0]
                result = get_taxonomy(taxonomy_conn, accession) or \
                         get_taxonomy(protein_conn, accession) or \
                         get_taxonomy(dead_conn, accession)

                if result != 'not found' and str(result[1]) in filter_dict:
                    filtered.write(f">{record.id}\n{record.seq}\n")


def main():
    """Main function to initialize script execution."""
    print("Start:", datetime.utcnow())
    options = usr_args()
    protein_conn, dead_conn, taxonomy_conn = create_connection(options.database)
    if not all([protein_conn, dead_conn, taxonomy_conn]):
        print("Error: Could not establish all database connections.")
        sys.exit(1)
    
    filter_dict = read_list(options.list)
    filter_nt(protein_conn, dead_conn, taxonomy_conn, options.nt, filter_dict, options.output, options.stats, options.mode)
    print("Filtering complete:", datetime.utcnow())


if __name__ == '__main__':
    main()
