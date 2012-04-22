"""Usage: example.py [-vqr] [FILE]

Options:
  -v  print status messages
  -q  report only file names
  -r  show all occurrences of the same error

"""
from docopt import docopt, Options, Arguments


def test_docopt():

    o, a = docopt(__doc__, '-v file.py')
    assert o == Options(v=True, q=False, r=False)
    assert a == Arguments(file='file.py')

    o, a = docopt(__doc__, '-v')
    assert o == Options(v=True, q=False, r=False)
    assert a == Arguments(file=None)
