"""Usage: prog [-vqr] [FILE]
          prog INPUT OUTPUT
          prog --help

Options:
  -v  print status messages
  -q  report only file names
  -r  show all occurrences of the same error
  --help

"""
from docopt import docopt, Options, Arguments, DocoptExit
from pytest import raises

def test_docopt():

    o, a = docopt(__doc__, '-v file.py')
    assert o == Options(v=True, q=False, r=False, help=False)
    assert a == Arguments(file='file.py', input=None, output=None)

    o, a = docopt(__doc__, '-v')
    assert o == Options(v=True, q=False, r=False, help=False)
    assert a == Arguments(file=None, input=None, output=None)

    with raises(DocoptExit):  # does not match
        docopt(__doc__, '-v input.py output.py')

    with raises(DocoptExit):
        docopt(__doc__, '--fake')

    with raises(SystemExit):
        docopt(__doc__, '--hel')
