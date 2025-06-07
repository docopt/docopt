"""Tests for command semantics."""

from .util import run_docopt
import pytest


def test_basic_command():
    usage = 'Usage: prog add'
    assert run_docopt(usage, 'add') == {'add': True}

def test_commands_multi():
    usage = 'Usage: prog (add|rm)'
    assert run_docopt(usage, 'add') == {'add': True, 'rm': False}
    assert run_docopt(usage, 'rm') == {'add': False, 'rm': True}
    usage = 'Usage: prog a b'
    assert run_docopt(usage, 'a b') == {'a': True, 'b': True}
    with pytest.raises(SystemExit):
        run_docopt('Usage: prog a b', 'b a')

