#!/usr/bin/env python3
"""Get Parent TaxID of BlackList

    This script generates a black list of unwanted taxonomy names (scientific names) from names.dmp
    and all child taxonomy names: ['unclassified','unidentified','uncultured','unspecified','unknown',
    'phage','vector'] and ['environmental sample','artificial sequence','other sequence'].

    input: path for the `names.dmp` file.

    output: hard-coded
    - The `blacklist-taxId.1.csv` is generated and used as input for the 
    `get-chiled-taxid-of-blacklist.py` script.

    usage: python get-parent-taxid-of-blacklist.py sort -u
        Deletes duplicated records, and store them
        into: /data/projects/targetdbs/generated/blacklist-taxId.unique.csv
"""
import sys
from argparse import ArgumentParser, SUPPRESS

__version__ = "2.0"
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
        prog='get-parent-taxid-of-blacklist.py',
        description="This scriptgenerates a black list of unwanted taxonomy"
        "names (scientific names) from names.dmp and all child taxonomy names:"
        "['unclassified','unidentified','uncultured','unspecified','unknown',"
        "'phage','vector'] and ['environmental sample','artificial sequence',"
        "'other sequence'].")

    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument('-n', '--name',
        required=True,
        help="'names.dmp' file. Should contain taxonomy names (scientific"
        " names) from NCBI. Default is `./data_raw/taxdump/names.dmp`",
        default='./data_raw/taxdump/names.dmp')


    optional.add_argument('-b', '--blacklist',
        help="Output file to create. The `blacklist-taxId.1.csv` is generated"
        "and used as input for the `get-chiled-taxid-of-blacklist.py` script."
        "Default is `./data_output/blacklist-taxId.1.csv` ",
        default='./data_output/blacklist-taxId.1.csv')
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

def read_names(name, blacklist):
    """Read Names



    Parameters
    ----------
    name: str
        filepath for the `names.dmp` file to be parsed
    blacklist: string
        filepath for the resulting blacklist file.

    Returns
    -------
        writes a CSV file at the indicated filepath. 
    """

    black_name = [
        "unclassified",
        "unidentified",
        "uncultured",
        "unspecified",
        "unknown",
        "phage",
        "vector",
    ]
    black_name2 = ["environmental sample", "other sequence"]

    with open(name, "r", encoding='utf-8') as read:
        for line1 in read:
            deter = False
            line = line1.strip().split("|")
            feature_type = line[3].strip()
            feature_name1 = line[1].lower().strip().split()
            feature_name2 = line[1].lower().strip()
            class_name = ""
            for j in black_name2:
                if (
                    feature_name2.find(j) >= 0
                    and line1.lower().find("scientific name") >= 0
                ):
                    deter = True
                    class_name += j + ";"
            for i in black_name:
                if i in feature_name1 and line1.lower().find("scientific name") >= 0:
                    deter = True
                    class_name += i + ";"
            if deter:
                # import pdb; pdb.set_trace()
                with open(blacklist, "a", encoding='utf-8') as write:
                    write.write(
                        line[0].strip()
                        + ","
                        + class_name[:-1]
                        + ","
                        + line[1].strip()
                        + "\n"
                    )

def main():
    """
    Main function
    """

    options = usr_args()
    read_names(options.name, options.blacklist)

if __name__ == "__main__":
    main()
