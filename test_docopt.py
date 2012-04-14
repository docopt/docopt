from docopt import (Option, Namespace, docopt, parse, Argument, VerticalBar,
                    Parens, Brackets, pattern, OneOrMore)


def test_option():
    assert Option(parse='-h') == Option('h', None)
    assert Option(parse='--help') == Option(None, 'help')
    assert Option(parse='-h --help') == Option('h', 'help')
    assert Option(parse='-h, --help') == Option('h', 'help')

    assert Option(parse='-h TOPIC') == Option('h:', None)
    assert Option(parse='--help TOPIC') == Option(None, 'help=')
    assert Option(parse='-h TOPIC --help TOPIC') == Option('h:', 'help=')
    assert Option(parse='-h TOPIC, --help TOPIC') == Option('h:', 'help=')
    assert Option(parse='-h TOPIC, --help=TOPIC') == Option('h:', 'help=')

    assert Option(parse='-h  Description...') == Option('h', None)
    assert Option(parse='-h --help  Description...') == Option('h', 'help')
    assert Option(parse='-h TOPIC  Description...') == Option('h:', None)

    assert Option(parse='    -h') == Option('h', None)

    assert Option(parse='-h TOPIC  Descripton... [default: 2]') == \
               Option('h:', None, 2)
    assert Option(parse='-h TOPIC  Descripton... [default: topic-1]') == \
               Option('h:', None, 'topic-1')
    assert Option(parse='--help=TOPIC  ... [default: 3.14]') == \
               Option(None, 'help=', 3.14)
    assert Option(parse='-h, --help=DIR  ... [default: "./"]') == \
               Option('h:', 'help=', "./")


def test_option_name():
    assert Option('h').name == 'h'
    assert Option('h', 'help').name == 'help'
    assert Option('h:', 'help=').name == 'help'
    assert Option('h', 'help-me').name == 'help_me'
    assert Option('2', '2-times').name == '__times'


def test_docopt():
    assert docopt('\n-v  Be verbose.', ['-v']) == (Namespace(v=True), [])
    assert docopt('-v  Be verbose.', ['-v']) == (Namespace(v=True), [])


def test_parse():

    o = [Option('h'),
         Option('v', 'verbose'),
         Option('f:', 'file=')]

    assert parse('') == []
    assert parse('-h', options=o) == [Option('h', None, True)]
    assert parse('-h --verbose', options=o) == \
            [Option('h', None, True), Option('v', 'verbose', True)]
    assert parse('-h --file f.txt', options=o) == \
            [Option('h', None, True), Option('f:', 'file=', 'f.txt')]
    assert parse('-h --file f.txt arg', options=o) == \
            [Option('h', None, True),
             Option('f:', 'file=', 'f.txt'),
             Argument(None, 'arg')]
    assert parse('-h --file f.txt arg arg2', options=o) == \
            [Option('h', None, True),
             Option('f:', 'file=', 'f.txt'),
             Argument(None, 'arg'),
             Argument(None, 'arg2')]

    assert pattern('[ -h ]', options=o) == \
               [Brackets(Option('h', None, True))]
    assert pattern('[ arg ... ]', options=o) == \
               [Brackets(OneOrMore(Argument(None, 'arg')))]
    assert pattern('[ -h | -v ]', options=o) == \
               [Brackets(Option('h', None, True), VerticalBar,
                        Option('v', 'verbose', True))]
    assert pattern('( -h | -v [ --file f.txt ] )', options=o) == \
               [Parens(Option('h', None, True), VerticalBar,
                        Option('v', 'verbose', True),
                        Brackets(Option('f:', 'file=', 'f.txt')))]
    assert pattern('(-h|-v[--file=f.txt]N...)', options=o) == \
               [Parens(Option('h', None, True),
                       VerticalBar,
                       Option('v', 'verbose', True),
                       Brackets(Option('f:', 'file=', 'f.txt')),
                       OneOrMore(Argument(None, 'N')))]


def test_option_match():
    assert Option('a').match([Option('a')]) == (True, [])
    assert Option('a').match([Option('x')]) == (False, [Option('x')])
    assert Option('a').match([Argument('N')]) == (False, [Argument('N')])
    assert Option('a').match([Option('x'), Option('a'), Argument('N')]) == \
            (True, [Option('x'), Argument('N')])
    assert Option('a', None, False).match([Option('a', None, False)]) == \
            (True, [])


def test_argument_match():
    assert Argument('N').match([Argument(None, 9)]) == (True, [])
    assert Argument('N').match([Option('x')]) == (False, [Option('x')])
    assert Argument('N').match([Option('x'), Option('a'), Argument('N')]) == \
            (True, [Option('x'), Option('a')])
    assert Argument('N').match([Argument(None, 9), Argument(None, 0)]) == \
            (True, [Argument(None, 0)])


def test_brackets_match():
    assert Brackets(Option('a')).match([Option('a')]) == (True, [])
    assert Brackets(Option('a')).match([]) == (True, [])
    assert Brackets(Option('a')).match([Option('x')]) == (True, [Option('x')])
    assert Brackets(Option('a'), Option('b')).match([Option('a')]) == \
            (True, [])
    assert Brackets(Option('a'), Option('b')).match([Option('b')]) == \
            (True, [])
    assert Brackets(Option('a'), Option('b')).match([Option('x')]) == \
            (True, [Option('x')])


def test_parens_match():
    assert Parens(Option('a')).match([Option('a')]) == (True, [])
    assert Parens(Option('a')).match([]) == (False, [])
    assert Parens(Option('a')).match([Option('x')]) == (False, [Option('x')])
    assert Parens(Option('a'), Option('b')).match([Option('a')]) == \
            (False, [])  # [] or [Option('a') ?
    assert Brackets(Option('a'), Option('b')).match(
            [Option('b'), Option('x'), Option('a')]) == (True, [Option('x')])


def test_one_or_more_match():
    assert OneOrMore(Argument('N')).match([Argument(None, 9)]) == (True, [])
    assert OneOrMore(Argument('N')).match([]) == (False, [])
    assert OneOrMore(Argument('N')).match([Option('x')]) == \
            (False, [Option('x')])
    assert OneOrMore(Argument('N')).match(
            [Argument(None, 9), Argument(None, 8)]) == (True, [])
    assert OneOrMore(Argument('N')).match(
            [Argument(None, 9), Option('x'), Argument(None, 8)]) == \
                    (True, [Option('x')])
    assert OneOrMore(Option('a')).match(
            [Option('a'), Argument(None, 8), Option('a')]) == \
                    (True, [Argument(None, 8)])
    assert OneOrMore(Option('a')).match([Argument(None, 8), Option('x')]) == \
                    (False, [Argument(None, 8), Option('x')])
    assert OneOrMore(Parens(Option('a'), Argument('N'))).match(
            [Option('a'), Argument(None, 1), Option('x'),
             Option('a'), Argument(None, 2)]) == (True, [Option('x')])


def test_basic_pattern_matching():
    # ( -a N [ -x Z ] )
    pattern = Parens(Option('a'), Argument('N'),
                     Brackets(Option('x'), Argument('Z')))
    # -a N
    assert pattern.match([Option('a'), Argument(None, 9)]) == (True, [])
    # -a -x N Z
    assert pattern.match([Option('a'), Option('x'),
                          Argument(None, 9), Argument(None, 5)]) == (True, [])
    # -x N Z  # BZZ!
    assert pattern.match([Option('x'),
                          Argument(None, 9), Argument(None, 5)]) == (False, [])
