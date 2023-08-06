import sys
from optparse import OptionParser


def parse_cmd_line():
    parser = OptionParser()
    parser.add_option(
        "--force",
        action="store_true",
        help="overwite output directly if it exists",
        default=False,
    )
    parser.add_option(
        "-l",
        "--live",
        action="store_false",
        dest="live",
        default=False,
        help="print file operations while running",
    )
    parser.add_option(
        "-o", "--output-file", dest="output", help="output to file instead of stderr"
    )
    parser.add_option(
        "-x", "--exclude", dest="exclude", help="exclude path from lookups", default=""
    )
    options, args = parser.parse_args()
    if len(args) < 2:
        print("Usage: {} output_directory -- command".format(sys.argv[0]))
        exit(1)
    return options, args
