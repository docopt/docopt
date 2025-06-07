"""Tests for [options] shortcut and -- handling."""

from .util import run_docopt
import pytest


def test_options_shortcut():
    usage = """Usage: prog [options]\nOptions: -h"""
    assert run_docopt(usage, '') == {'-h': False}


def test_issue_68_options_shortcut_does_not_include_options_in_usage_pattern():
    args = run_docopt('usage: prog [-ab] [options]\noptions: -x\n -y', '-ax')
    assert args['-a'] is True
    assert args['-b'] is False
    assert args['-x'] is True
    assert args['-y'] is False


def test_double_dash_stops_option_parsing():
    usage = 'Usage: prog [-o] [--] <arg>\nOptions: -o'
    assert run_docopt(usage, '-- -v') == {'-o': False, '<arg>': '-v', '--': True}
    with pytest.raises(SystemExit):
        run_docopt('Usage: prog [-o] <arg>\nOptions: -o', '-- -v')

