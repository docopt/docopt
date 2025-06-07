"""Tests for short and long options handling."""

from .util import run_docopt
from docopt import Option


def test_option_parse_simple():
    assert Option.parse('-h') == Option('-h', None)
    assert Option.parse('--help') == Option(None, '--help')
