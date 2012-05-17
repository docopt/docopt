"""Usage: odd_even_example.py (ODD EVEN)...

Example:
  odd_even_example.py 1 2 3 4

"""
from docopt import docopt


if __name__ == '__main__':
    options, arguments = docopt(__doc__)
    print(arguments)
