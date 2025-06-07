"""Tests for positional argument parsing."""

from docopt import Argument, docopt


def test_argument_equality():
    assert Argument("N") == Argument("N")

