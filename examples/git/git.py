"""Subset of git CLI.

Usage: git.py [--version] [--exec-path[=<path>]] [--html-path]
              [-p|--paginate|--no-pager] [--no-replace-objects]
              [--bare] [--git-dir=<path>] [--work-tree=<path>]
              [-c name=value]
              <command> [options] [<args>...]
       git.py (-h | --help)

"""
import sys
from subprocess import call

from docopt import docopt


if __name__ == '__main__':

    args = docopt(__doc__,
                  version='git version 1.7.4.4',
                  help=False,
                  _any_options=True)

    # Handle -h|--help manually.
    # Otherwise `subcommand -h` would trigger global help.
    if args['<command>'] is None and (args.get('-h') or args.get('--help')):
        print(__doc__.strip())
        exit()

    # Make argv for subparsers that does not include global options:
    i = sys.argv.index(args['<command>'])
    sub_argv = sys.argv[i:]

    if args['<command>'] == 'add':
        # In case subcommand is implemented as python module:
        import git_add
        print(docopt(git_add.__doc__, argv=sub_argv))
    elif args['<command>'] == 'commit':
        # In case subcommand is a script in some other programming language:
        exit(call(['python', 'git_commit.py'] + sub_argv))
    elif args['<command>'] == 'push':
        exit(call(['python', 'git_push.py'] + sub_argv))
    elif args['<command>'] == 'help':
        exit(call(['python', 'git.py'] + args['<args>'] + ['-h']))
    else:
        exit("%r is not a git.py command. See 'git help'." % args['<command>'])
