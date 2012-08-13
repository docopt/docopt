"""Example dispatching multiple scripts with several help-screens.

Usage:
    delegation_example.py <command> [options] [<arguments>...]
    delegation_example.py (-h | --help)

Commands:
    add
    remove

See `help <command>` for help on each command.

"""
from docopt import docopt


add_help = """Add command.

Usage: delegation_example.py add <this> [<and-that>] [--local]

"""


remove_help = """Remove command.

Usage: delegation_example.py remove <that> <from-this>

"""

args = docopt(__doc__)#, _delegate=True)
if args['<command>'] == 'add':
    args = docopt(add_help)
    print(args)
elif args['<command>'] == 'remove':
    args = docopt(remove_help)
    print(args)
