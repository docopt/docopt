"""

Usage: git add [-n] [-v] [--force | -f] [--interactive | -i] [--patch | -p]
               [--edit | -e] [--all | [--update | -u]] [--intent-to-add | -N]
               [--refresh] [--ignore-errors] [--ignore-missing] [--]
               <filepattern>...
       git add (-h | --help)

Options:
    -h, --help
    -f, --force
    -i, --interactive
    -p, --patch
    -e, --edit
    -u, --update
    -N, --intent-to-add

"""
from docopt import docopt


if __name__ == '__main__':
    print(docopt(__doc__))
