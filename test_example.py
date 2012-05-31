"""Usage: prog [-vqr] [FILE]
          prog INPUT OUTPUT
          prog --help

Options:
  -v  print status messages
  -q  report only file names
  -r  show all occurrences of the same error
  --help

"""
from __future__ import with_statement
from docopt import docopt, DocoptExit
from pytest import raises

def test_docopt():

    a = docopt(__doc__, '-v file.py')
    assert a == {'-v': True, '-q': False, '-r': False, '--help': False,
                 'FILE': 'file.py', 'INPUT': None, 'OUTPUT': None}

    a = docopt(__doc__, '-v')
    assert a == {'-v': True, '-q': False, '-r': False, '--help': False,
                 'FILE': None, 'INPUT': None, 'OUTPUT': None}

    with raises(DocoptExit):  # does not match
        docopt(__doc__, '-v input.py output.py')

    with raises(DocoptExit):
        docopt(__doc__, '--fake')

    with raises(SystemExit):
        docopt(__doc__, '--hel')
