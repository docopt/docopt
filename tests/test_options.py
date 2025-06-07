"""Tests for short and long options handling."""

from .util import run_docopt
from docopt import Option
import pytest


def test_option_parse_simple():
    assert Option.parse('-h') == Option('-h', None)
    assert Option.parse('--help') == Option(None, '--help')


def test_option_parsing_extended():
    assert Option.parse('-h --help') == Option('-h', '--help')
    assert Option.parse('-h, --help') == Option('-h', '--help')
    assert Option.parse('-h TOPIC') == Option('-h', None, 1)
    assert Option.parse('--help TOPIC') == Option(None, '--help', 1)
    assert Option.parse('-h TOPIC --help TOPIC') == Option('-h', '--help', 1)
    assert Option.parse('-h TOPIC, --help TOPIC') == Option('-h', '--help', 1)
    assert Option.parse('-h TOPIC, --help=TOPIC') == Option('-h', '--help', 1)
    assert Option.parse('-h  Description...') == Option('-h', None)
    assert Option.parse('-h --help  Description...') == Option('-h', '--help')
    assert Option.parse('-h TOPIC  Description...') == Option('-h', None, 1)
    assert Option.parse('    -h') == Option('-h', None)
    assert Option.parse('-h TOPIC  Descripton... [default: 2]') == \
        Option('-h', None, 1, '2')
    assert Option.parse('-h TOPIC  Descripton... [default: topic-1]') == \
        Option('-h', None, 1, 'topic-1')
    assert Option.parse('--help=TOPIC  ... [default: 3.14]') == \
        Option(None, '--help', 1, '3.14')
    assert Option.parse('-h, --help=DIR  ... [default: ./]') == \
        Option('-h', '--help', 1, './')
    assert Option.parse('-h TOPIC  Descripton... [dEfAuLt: 2]') == \
        Option('-h', None, 1, '2')

def test_option_name():
    assert Option('-h', None).name == '-h'
    assert Option('-h', '--help').name == '--help'
    assert Option(None, '--help').name == '--help'

def test_count_multiple_flags():
    assert run_docopt('usage: prog [-v]', '-v') == {'-v': True}
    assert run_docopt('usage: prog [-vv]', '') == {'-v': 0}
    assert run_docopt('usage: prog [-vv]', '-v') == {'-v': 1}
    assert run_docopt('usage: prog [-vv]', '-vv') == {'-v': 2}
    with pytest.raises(SystemExit):
        run_docopt('usage: prog [-vv]', '-vvv')
    assert run_docopt('usage: prog [-v | -vv | -vvv]', '-vvv') == {'-v': 3}
    assert run_docopt('usage: prog -v...', '-vvvvvv') == {'-v': 6}
    assert run_docopt('usage: prog [--ver --ver]', '--ver --ver') == {'--ver': 2}


def test_option_defaults_and_repeats():
    doc = """Usage: prog [--path=<p>...]
Options:
    --path=<p>  Path [default: a b]
"""
    result = run_docopt(doc, '')
    assert result == {'--path': ['a', 'b']}
    result = run_docopt(doc, '--path=c --path=d')
    assert result == {'--path': ['c', 'd']}

