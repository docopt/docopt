"""Usage: arguments_example.py [-vqrh] [FILE] ...
          arguments_example.py (--left | --right) CORRECTION FILE

Process FILE and optionally apply correction to either left-hand side or
right-hand side.

Arguments:
  FILE        optional input file
  CORRECTION  correction angle, needs FILE, --left or --right to be present

Options:
  -h --help
  -v       verbose mode
  -q       quiet mode
  -r       make report
  --left   use left-hand side
  --right  use right-hand side

"""
from docopt import docopt


if __name__ == "__main__":
    arguments = docopt(__doc__)
    print(arguments)
