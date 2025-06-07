"""Tests for Usage and Options sections parsing."""

from docopt import parse_section


def test_parse_section_usage():
    text = '\nUsage: prog\n\nOptions:\n -h'
    assert parse_section('usage:', text) == ['Usage: prog']


def test_parse_section_complex():
    usage = '''usage: this

usage:hai
usage: this that

usage: foo
       bar

PROGRAM USAGE:
 foo
 bar
usage:
\ttoo
\ttar
Usage: eggs spam
BAZZ
usage: pit stop'''
    assert parse_section('usage:', 'foo bar fizz buzz') == []
    assert parse_section('usage:', 'usage: prog') == ['usage: prog']
    assert parse_section('usage:', 'usage: -x\n -y') == ['usage: -x\n -y']
    assert parse_section('usage:', usage) == [
        'usage: this',
        'usage:hai',
        'usage: this that',
        'usage: foo\n       bar',
        'PROGRAM USAGE:\n foo\n bar',
        'usage:\n\ttoo\n\ttar',
        'Usage: eggs spam',
        'usage: pit stop',
    ]

from docopt import parse_defaults, Option


def test_issue_126_defaults_not_parsed_correctly_when_tabs():
    section = 'Options:\n\t--foo=<arg>  [default: bar]'
    assert parse_defaults(section) == [Option(None, '--foo', 1, 'bar')]

