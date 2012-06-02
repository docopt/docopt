"""Usage:
    git_example.py remote [-v | --verbose]
    git_example.py remote add [-t <branch>] [-m <master>] [-f]
                   [--tags|--no-tags] [--mirror] <name> <url>
    git_example.py remote rename <old> <new>
    git_example.py remote rm <name>
    git_example.py remote set-head <name> (-a | -d | <branch>)
    git_example.py remote set-branches <name> [--add] <branch>...
    git_example.py remote set-url [--push] <name> <newurl> [<oldurl>]
    git_example.py remote set-url --add [--push] <name> <newurl>
    git_example.py remote set-url --delete [--push] <name> <url>
    git_example.py remote [-v | --verbose] show [-n] <name>
    git_example.py remote prune [-n | --dry-run] <name>
    git_example.py remote [-v | --verbose] update [-p | --prune]
                   [(<group> | <remote>)...]

Options:
    -v, --verbose
    -t <branch>
    -m <master>
    -f
    --tags
    --no-tags
    --mittor
    -a
    -d
    -n, --dry-run
    -p, --prune
    --add
    --delete
    --push
    --mirror

"""
from docopt import docopt


if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)
