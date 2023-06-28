#!/usr/bin/env python3

"""Filter NT

This script filters the nt files that were manually added in ac2taxids. 

Input
^^^^^
All inputs are currently hard-coded. 
- `ntFile`: path for the downloaded ntFile ../nt.DATE
- `ac2taxidFile`: path for the generated ac2taxid text file ../logfile.ac2taxid.list.txt
- `ac2taxidFile2`: path for manually added logfile ../logfile.step3.manually.added.txt
- `blackFile`: path for Blacklist csv file ../blacklist-taxId.unique.csv

Output
^^^^^^
All outputs are currently hard-coded. 
- The `filtered_nt_June6-2017.fasta` is generated. 
	- Contains the final filterend nucleotide sequences in FASTA format.

Usage
^^^^^
- Currently no options available.
"""

import sys
import csv
from datetime import datetime
import sqlite3
from sqlite3 import Error
from argparse import ArgumentParser, SUPPRESS
from Bio import SeqIO

__version__="1.0"
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
        prog='filter-nt.py',
        description="This script filters the nt files that were manually"
			"added in ac2taxids.")

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument('-n', '--nt',
        help="Path to `nt` file.",
        default='./raw_data/nt'
        )
 
    required.add_argument('-d', '--database',
        help="'db.sqlite3' files. Should contain path to DB files",
        default='./output_data'
        )

    required.add_argument('-o', '--output',
        help="Log file file to create."
        "Default is `./output_data/filteredNT.fasta` ",
        default='./output_data/filteredNT.fasta')

    required.add_argument('-b', '--blacklist',
        help="path for Blacklist csv file.",
        default='./output_data/blacklist_unique.csv')
    
    required.add_argument('-s', '--stats',
        help="path for Blacklist stats tsv file.",
        default='./output_data/blackstats.tsv')

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

def read_blacklist(blacklist:str) -> dict: 
    """Read Blacklist
    
    Populates a dictionary with the blacklisted TaxIds
    """
    black_dict = {}
    with open(blacklist, 'r', encoding='utf-8') as list:
        reader =  csv.reader(list, delimiter=',')
        for row in reader:
            black_dict[row[0]] = row[1], row[2]
    print('Blacklist loaded: ', datetime.utcnow())
    return black_dict

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

def filter_nt(protein_conn, dead_conn, taxonomy_conn, nt, black_dict, outfile):
    """Filter NT"""
    
    black_stats = {}
    with open(outfile, 'w', encoding='utf-8') as filtered:
        count = 0
        for record in SeqIO.parse(nt, 'fasta'):
            count += 1
            prot_result, tax_result, dead_result = '', '', ''
            accession = record.id.split('.')[0]
            result = get_taxonomy(taxonomy_conn, accession)
            # import pdb; pdb.set_trace()
            if result == 'not found':
                result = get_taxonomy(protein_conn, accession)
                if result == 'not found':
                    result = get_taxonomy(dead_conn, accession)
                    if result == 'not found':
                        raise f'{accession} Not Found'
            if str(result[1]) in black_dict.keys():
                    black_stats[accession] = result[1], black_dict[str(result[1])][0], black_dict[str(result[1])][1]  
            else:
                filtered.write(">%s\n%s\n" % (record.id, record.seq))
                
            # if len(black_stats) == 10000:
            #     return black_stats

def write_blackstats(blackstats: dict, stats:str):
    """Write Blacklist stats
    """

    with open(stats, 'w', encoding='utf-8')as stat_file:
        writer = csv.writer(stat_file, delimiter='\t')
        writer.writerow(['accession','taxid', 'node', 'name'])
        for key, value in blackstats.items():
            writer.writerow([key, value[0], value[1], value[2]])

def main():
    """Main Function"""

    print('Start: ', datetime.utcnow())
    options = usr_args()
    protein_conn, dead_conn, taxonomy_conn = create_connection(options.database)
    black_dict = read_blacklist(options.blacklist)
    blackstats = filter_nt(protein_conn, dead_conn, taxonomy_conn, options.nt, black_dict, options.output)
    write_blackstats(blackstats, options.stats)

if __name__ == '__main__':
    main()
