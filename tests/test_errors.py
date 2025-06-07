"""Language and runtime error tests."""

from pytest import raises
from docopt import DocoptLanguageError


def test_unmatched_parenthesis():
    with raises(DocoptLanguageError):
        from docopt import docopt
        docopt('Usage: prog (', '')
