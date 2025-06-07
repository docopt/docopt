"""Low level parser component tests."""

from docopt import DocoptExit
from docopt import parse_argv, Option, Argument, Command, OptionsShortcut, Required, Optional, Either, OneOrMore
from docopt import parse_pattern, Tokens


def test_parse_pattern_literal():
    result = parse_pattern('N', Tokens('N'))
    assert str(result) == "Required(Argument('N', None))"


def test_parse_argv_complex():
    o = [Option('-h'), Option('-v', '--verbose'), Option('-f', '--file', 1)]
    TS = lambda s: Tokens(s, error=DocoptExit)
    assert parse_argv(TS(''), options=o) == []
    assert parse_argv(TS('-h'), options=o) == [Option('-h', None, 0, True)]
    assert parse_argv(TS('-h --verbose'), options=o) == [
        Option('-h', None, 0, True), Option('-v', '--verbose', 0, True)
    ]
    assert parse_argv(TS('-h --file f.txt'), options=o) == [
        Option('-h', None, 0, True), Option('-f', '--file', 1, 'f.txt')
    ]


def test_parse_pattern_options():
    o = [Option('-h'), Option('-v', '--verbose'), Option('-f', '--file', 1)]
    assert parse_pattern('[ -h ]', options=o) == Required(Optional(Option('-h')))
    assert parse_pattern('[ ARG ... ]', options=o) == Required(
        Optional(OneOrMore(Argument('ARG')))
    )
    assert parse_pattern('[options]', options=o) == Required(Optional(OptionsShortcut()))

