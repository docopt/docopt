"""

Usage: git_commit [-a | --interactive] [-s] [-v] [-u <mode>] [--amend]
                  [--dry-run] [-c <commit> | -C <commit> | --fixup=<commit>
                   | --squash=<commit>]
                  [-F <file> | -m <msg>] [--reset-author] [--allow-empty]
                  [--allow-empty-message] [--no-verify] [-e]
                  [--author=<author>] [--date=<date>] [--cleanup=<mode>]
                  [--status | --no-status] [-i | -o] [--] [<file>...]
       git commit (-h | --help)

Options:
    -u <mode>
    -c <commit>
    -C <commit>
    -F <file>
    -m <msg>

"""
from docopt import docopt


if __name__ == '__main__':
    print(docopt(__doc__))
