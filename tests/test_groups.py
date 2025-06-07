"""Tests for grouping constructs."""

from docopt import Required, Optional, Argument
from docopt import Option, Either, OneOrMore, Command


def test_group_flatten():
    group = Required(Optional(Argument('N')))
    assert group.flat() == [Argument('N')]


def test_optional_required_either():
    assert Optional(Option('-a')).match([Option('-a')]) == (True, [], [Option('-a')])
    assert Required(Option('-a')).match([]) == (False, [], [])
    assert Either(Option('-a'), Option('-b')).match([Option('-a')]) == (True, [], [Option('-a')])


def test_one_or_more_and_list_arguments():
    assert OneOrMore(Argument('N')).match([Argument(None, 9)]) == (True, [], [Argument('N', 9)])
    assert Required(Argument('N'), Argument('N')).fix().match([
        Argument(None, '1'), Argument(None, '2')]) == (True, [], [Argument('N', ['1', '2'])])

