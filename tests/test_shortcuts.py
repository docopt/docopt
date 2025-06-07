"""Tests for [options] shortcut and -- handling."""

from .util import run_docopt


def test_options_shortcut():
    usage = """Usage: prog [options]\nOptions: -h"""
    assert run_docopt(usage, '') == {'-h': False}
