"""Language and runtime error tests."""

from pytest import raises
from docopt import DocoptLanguageError


def test_unmatched_parenthesis():
    with raises(DocoptLanguageError):
        from docopt import docopt
        docopt('Usage: prog (', '')

from docopt import docopt, DocoptExit


def test_long_options_error_handling():
    with raises(DocoptExit):
        docopt('Usage: prog', '--non-existent')
    with raises(DocoptExit):
        docopt('Usage: prog [--version --verbose]\n',
               '--ver')
    with raises(DocoptLanguageError):
        docopt('Usage: prog --long\nOptions: --long ARG')
    with raises(DocoptExit):
        docopt('Usage: prog --long ARG\nOptions: --long ARG', '--long')
    with raises(DocoptLanguageError):
        docopt('Usage: prog --long=ARG\nOptions: --long')
    with raises(DocoptExit):
        docopt('Usage: prog --long\nOptions: --long', '--long=ARG')


def test_short_options_error_handling():
    with raises(DocoptLanguageError):
        docopt('Usage: prog -x\nOptions: -x  this\n -x  that')
    with raises(DocoptExit):
        docopt('Usage: prog', '-x')
    with raises(DocoptLanguageError):
        docopt('Usage: prog -o\nOptions: -o ARG')
    with raises(DocoptExit):
        docopt('Usage: prog -o ARG\nOptions: -o ARG', '-o')


def test_language_errors():
    with raises(DocoptLanguageError):
        docopt('no usage with colon here')
    with raises(DocoptLanguageError):
        docopt('usage: here \n\n and again usage: here')


def test_issue_40():
    with raises(SystemExit):
        docopt('usage: prog --help-commands | --help', '--help')
    assert docopt('usage: prog --aabb | --aa', '--aa') == {'--aabb': False, '--aa': True}


def test_issue_71_double_dash_is_not_a_valid_option_argument():
    with raises(DocoptExit):
        docopt('usage: prog [--log=LEVEL] [--] <args>...', '--log -- 1 2')
    with raises(DocoptExit):
        docopt('usage: prog [-l LEVEL] [--] <args>...\noptions: -l LEVEL', '-l -- 1 2')

