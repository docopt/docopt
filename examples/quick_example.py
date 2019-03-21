"""Usage:
  quick_example.py tcp <host> <port> [--timeout=<seconds>]
  quick_example.py serial <port> [--baud=9600] [--timeout=<seconds>]
  quick_example.py -h | --help | --version

"""
from docopt import docopt


if __name__ == "__main__":
    arguments = docopt(__doc__, version="0.1.1rc")
    print(arguments)
