"""Example of program with many commands.

Usage:
  commands_example.py ship move (up|down|left|right) [--fast]
  commands_example.py ship shoot <x> <y>
  commands_example.py mine (set|remove) <x> <y>
  commands_example.py (-h | --help)

Options:
  -h --help  Show help screen.
  --fast     Move ship *fast*.

"""
from docopt import docopt


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Naval Fate 2.0')
    print(arguments)
