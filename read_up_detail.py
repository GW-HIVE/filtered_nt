#!/usr/bin/env python3

"""Read Uniprot Detail

This script reads a Uniprot proteome detail JSON file and returns the NCBI accessions. 

"""

import sys
import json
from datetime import datetime
from argparse import ArgumentParser, SUPPRESS

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
        prog='read_up_detail.py',
        description="This script reads a Uniprot proteome detail JSON file and"
        "returns the NCBI accessions.")

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument('-j', '--json',
        help="Path to `json` file.",
        default='./output_data/results.json'
        )
    required.add_argument('-o', '--output',
        help="New accession list file to create.",
        default='./output_data/ncbi_accessions.txt')

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


def main():
    """Main Function"""

    # print('Start: ', datetime.utcnow())
    options = usr_args()
    count = 0
    empty = 0
    with open(options.json) as infile:
        data = json.load(infile)
        for item in data:
            try:
                for component in item["components"]:
                    if "proteomeCrossReferences" in component:
                        for xref in component["proteomeCrossReferences"]:
                            if xref['database'] == 'GenomeAccession':
                                count += 1
                                print(xref["id"])
            except KeyError as error:
                empty += 1
                print(error)
                # import pdb; pdb.set_trace()
            #     pass
    print("count = ", count, "empty =", empty)
if __name__ == '__main__':
    main()
