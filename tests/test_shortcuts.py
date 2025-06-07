"""Tests for [options] shortcut and -- handling."""

from .util import run_docopt


def test_options_shortcut():
    usage = """Usage: prog [options]\nOptions: -h"""
    assert run_docopt(usage, '') == {'-h': False}


def test_issue_68_options_shortcut_does_not_include_options_in_usage_pattern():
    args = run_docopt('usage: prog [-ab] [options]\noptions: -x\n -y', '-ax')
    assert args['-a'] is True
    assert args['-b'] is False
    assert args['-x'] is True
    assert args['-y'] is False

