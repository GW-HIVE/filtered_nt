#!/usr/bin/env python3
"""Blacklist stats

"""

import sys
import csv
from datetime import datetime
from argparse import ArgumentParser, SUPPRESS

__version__ = "7.0"
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
        prog='blackstats.py',
        description="This script counts the items from a black list of "
            "unwanted taxonomy names (scientific names). "
            "names: ['unclassified','unidentified','uncultured','unspecified',"
            "'unknown','phage','vector'] and ['environmental sample',"
            "'artificial sequence','other sequence'].")

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument('-b', '--blackstats',
        help="Input file to use. The `blackstats.tsv` is "
        "used to generate the filtering statistics. "
        "Default is `./output_data/blacklist-taxId.1.csv` ",
        default='./output_data/blackstats.tsv')

    optional.add_argument('-o', '--output',
        help="Output file to create."
        "Default is `./output_data/filter_stats.tsv` ",
        default='./output_data/filter_stats.tsv')

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

def read_blackstats(blackstats:str) -> dict: 
    """Read Blacklist statistics 
    
    Populates a dictionary with the blacklisted TaxIds
    and other terms to calculate overall statistics.
    """

    black_dict = {}
    with open(blackstats, 'r', encoding='utf-8') as list:
        reader =  csv.reader(list, delimiter='\t')
        next(reader)
        for row in reader:
            if row[2] in black_dict.keys():
                black_dict[row[2]][1] += 1
                if row[1] not in black_dict[row[2]][0]:
                    black_dict[row[2]][0].append(row[1])
            else:
                black_dict[row[2]] = [[row[1]], 1]
    print('Blacklist loaded: ', datetime.utcnow())
    return black_dict

def write_filter_stats(black_dict: dict, filter_stats:str):
    """Write Filter Stats
    """
    with open(filter_stats, 'w', encoding='utf-8') as stat_file:
        writer = csv.writer(stat_file, delimiter='\t')
        writer.writerow(['blackListTaxonomyName','taxid', 'removed sequences'])
        for key in black_dict.keys():
            writer.writerow([key, len(black_dict[key][0]), black_dict[key][1]])

def main():
    """Main Function"""

    options = usr_args()
    black_dict = read_blackstats(options.blackstats)
    write_filter_stats(black_dict, options.output)

if __name__ == '__main__':
    main()
