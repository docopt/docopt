"""Usage: odd_even_example.py [ODD EVEN] ...

"""
from docopt import docopt


if __name__ == '__main__':
    # try: odd_even_example.py 1 2 3 4 5 6 7 8 9 10
    options, arguments = docopt(__doc__)
    print(arguments)
