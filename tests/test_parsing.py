"""Low level parser component tests."""

from docopt import parse_pattern, Tokens


def test_parse_pattern_literal():
    result = parse_pattern('N', Tokens('N'))
    assert str(result) == "Required(Argument('N', None))"
