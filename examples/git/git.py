#! /usr/bin/env python
"""
usage: git [--version] [--exec-path=<path>] [--html-path]
           [-p|--paginate|--no-pager] [--no-replace-objects]
           [--bare] [--git-dir=<path>] [--work-tree=<path>]
           [-c <name>=<value>] [--help]
           <command> [<args>...]

options:
   -c <name=value>
   -h, --help
   -p, --paginate

The most commonly used git commands are:
   add        Add file contents to the index
   branch     List, create, or delete branches
   checkout   Checkout a branch or paths to the working tree
   clone      Clone a repository into a new directory
   commit     Record changes to the repository
   push       Update remote refs along with associated objects
   remote     Manage set of tracked repositories

See 'git help <command>' for more information on a specific command.

"""
from subprocess import call

from docopt import docopt


if __name__ == "__main__":

    args = docopt(__doc__, version="git version 1.7.4.4", options_first=True)
    print("global arguments:")
    print(args)
    print("command arguments:")

    argv = [args["<command>"]] + args["<args>"]
    if args["<command>"] == "add":
        # In case subcommand is implemented as python module:
        import git_add

        print(docopt(git_add.__doc__, argv=argv))
    elif args["<command>"] == "branch":
        # In case subcommand is a script in some other programming language:
        exit(call(["python", "git_branch.py"] + argv))
    elif args["<command>"] in "checkout clone commit push remote".split():
        # For the rest we'll just keep DRY:
        exit(call(["python", "git_%s.py" % args["<command>"]] + argv))
    elif args["<command>"] in ["help", None]:
        exit(call(["python", "git.py", "--help"]))
    else:
        exit("%r is not a git.py command. See 'git help'." % args["<command>"])
