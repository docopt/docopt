"""Tests for positional argument parsing."""

from docopt import Argument, docopt
import pytest


def test_argument_equality():
    assert Argument("N") == Argument("N")


def test_repeated_arguments():
    usage = "Usage: prog NAME..."
    assert docopt(usage, "alice bob") == {"NAME": ["alice", "bob"]}
    with pytest.raises(SystemExit):
        docopt(usage, "")


def test_optional_argument_list():
    usage = "Usage: prog [NAME ...]"
    assert docopt(usage, "alice bob") == {"NAME": ["alice", "bob"]}
    assert docopt(usage, "") == {"NAME": []}

