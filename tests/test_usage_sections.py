"""Tests for Usage and Options sections parsing."""

from docopt import parse_section


def test_parse_section_usage():
    text = '\nUsage: prog\n\nOptions:\n -h'
    assert parse_section('usage:', text) == ['Usage: prog']
