"""Example of allowing arbitrary options.

Usage:
  options_shortcut_example.py [options]

Here meaning of [options] is modified (by passing any_options=True
to docopt function) to mean any options, also those that are not
listed in a help message.

Try:
  options_shortcut_example.py --all --long --human-readable
  options_shortcut_example.py -alh
  options_shortcut_example.py --key=value --key another
  options_shortcut_example.py -vvv

"""
from docopt import docopt


if __name__ == '__main__':
    arguments = docopt(__doc__, _any_options=True)
    print(arguments)
