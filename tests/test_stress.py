"""Stress tests for complex patterns."""

from .util import run_docopt


def test_many_arguments():
    doc = 'Usage: prog ' + 'ARG ' * 20
    argv = ' '.join('v{}'.format(i) for i in range(20))
    result = run_docopt(doc, argv)
    assert all(result['ARG'][i] == 'v{}'.format(i) for i in range(20))
