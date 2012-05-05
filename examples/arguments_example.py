"""Usage: prog [-vqr] [FILE]
          prog (--left | --right) CORRECTION FILE
          prog --help

Options:
  --help
  -v       verbose mode
  -q       quiet mode
  -r       make report
  --left   use left-hand side
  --right  use right-hand side

"""
from docopt import docopt


def main(options, arguments):
    print(options)
    print(arguments)


if __name__ == '__main__':
    # parse options based on docstring above
    options, arguments = docopt(__doc__)
    main(options, arguments)
