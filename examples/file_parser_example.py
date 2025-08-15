"""
File Parser the Mighty!

Process all files in a path and output data to a CSV file or a MySQL database.

Usage: file_parser_example.py -input- -output- -misc-
       file_parser_example.py -h --help

  Input:
    -f FILE | (-d DIR [-r])

  Output:
    -o CSV | (-b DB -u USER -p PASS)

  Misc:
    [-v...]  affects only stdout, not the log file
    -l LOG   log file is required

Options:
  -l LOG, --log_file=LOG     path to log file [default: 123]
  -f FLE, --input_file=FILE  path to a file to parse
  -d DIR, --input_dir=DIR    path to input directory
  -r, --recursive            look for files in all subdirectories
  -o CSV, --output_file=CSV  path to output CSV file
  -b DB, --database=DB       name of MySQL database
  -u USER, --username=USER   username for access to database
  -p PASS, --password=PASS   password for USER
  -v         verbosity for stdout, specify 0 to 4 times for different levels
  -h --help  this help message

"""
from docopt import docopt


if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)
