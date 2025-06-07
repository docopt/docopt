"""Tests for command semantics."""

from .util import run_docopt


def test_basic_command():
    usage = 'Usage: prog add'
    assert run_docopt(usage, 'add') == {'add': True}
