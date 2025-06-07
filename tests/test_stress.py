"""Stress tests for complex patterns."""

from .util import run_docopt


def test_many_arguments():
    doc = 'Usage: prog ' + 'ARG ' * 20
    argv = ' '.join('v{}'.format(i) for i in range(20))
    result = run_docopt(doc, argv)
    assert all(result['ARG'][i] == 'v{}'.format(i) for i in range(20))


def test_many_options():
    count = 30
    usage = 'Usage: prog ' + ' '.join('[--opt{0}=<v{0}>]'.format(i) for i in range(count))
    options = '\n'.join('  --opt{0}=<v{0}>'.format(i) for i in range(count))
    doc = usage + '\n\nOptions:\n' + options
    argv = ' '.join('--opt{0}=val{0}'.format(i) for i in range(count))
    result = run_docopt(doc, argv)
    expected = {'--opt{0}'.format(i): 'val{0}'.format(i) for i in range(count)}
    assert result == expected


def test_nested_either_chain():
    depth = 10
    expr = 'cmd0'
    for i in range(1, depth):
        expr = 'cmd{0} | ({1})'.format(i, expr)
    doc = 'Usage: prog ' + expr
    argv = 'cmd{}'.format(depth - 1)
    result = run_docopt(doc, argv)
    for i in range(depth):
        assert result['cmd{}'.format(i)] == (i == depth - 1)
