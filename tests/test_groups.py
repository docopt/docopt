"""Tests for grouping constructs."""

from docopt import Required, Optional, Argument


def test_group_flatten():
    group = Required(Optional(Argument('N')))
    assert group.flat() == [Argument('N')]
