"""Usage: odd_even_example.py [-h | --help] (ODD EVEN)...

Example, try:
  odd_even_example.py 1 2 3 4

Options:
  -h, --help

"""
from docopt import docopt


if __name__ == '__main__':
    options, arguments = docopt(__doc__)
    print(arguments)
