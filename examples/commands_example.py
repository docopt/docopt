"""Example of program with many commands.

Usage:
  commands_example.py ship new <name>...
  commands_example.py ship [<name>] move (up|down|left|right) [--speed=<kn>]
  commands_example.py ship shoot <x> <y>
  commands_example.py mine (set|remove) <x> <y> [--moored|--drifting]
  commands_example.py -h | --help
  commands_example.py --version

Options:
  -h --help     Show help screen.
  --version     Show version.
  --speed=<kn>  Speed in knots
  --moored      Mored (anchored) mine.
  --drifting    Drifting mine.

"""
from docopt import docopt


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Naval Fate 2.0')
    print(arguments)
