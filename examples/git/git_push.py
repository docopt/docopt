"""

Usage: git push [--all | --mirror | --tags] [-n | --dry-run]
                [--receive-pack=<git-receive-pack>] [--repo=<repository>]
                [-f | --force] [-v | --verbose] [-u | --set-upstream]
                [<repository> [<refspec>...]]
       git push (-h | --help)

Options:
    -n, --dry-run
    -f, --force
    -v, --verbose
    -u, --set-upstream

"""
from docopt import docopt


if __name__ == '__main__':
    print(docopt(__doc__))
