"""Example of program which use [options] shortcut in pattern

Usage:
  any_options_example.py [options]

Options:
  -h --help                show this help message and exit
  --version                show version and exit
  -n, --number N           use N as a number
  -t, --timeout TIMEOUT    set timeout TIMEOUT seconds
  --apply                  apply changes to database
  -q                       operate in quiet mode

"""
from docopt import docopt


if __name__ == '__main__':
    options, arguments = docopt(__doc__, version='1.0.0rc2')
    print(options)
    print(arguments)
