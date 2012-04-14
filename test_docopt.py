from docopt import (Option, Options, docopt, Pattern, Argument, VerticalBar,
                    Parens, Brackets)


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
    assert docopt('\n-v  Be verbose.', ['-v']) == (Options(v=True), [])
    assert docopt('-v  Be verbose.', ['-v']) == (Options(v=True), [])


def test_pattern():

    o = [Option('h'),
         Option('v', 'verbose'),
         Option('f:', 'file=')]
    a = [Argument('A'),
         Argument('A2')]

    assert Pattern(parse='') == Pattern()
    assert Pattern(parse='-h', options=o) == \
               Pattern(Option('h', None, True))
    assert Pattern(parse='-h --verbose', options=o) == \
               Pattern(Option('h', None, True), Option('v', 'verbose', True))
    assert Pattern(parse='-h --file f.txt', options=o) == \
               Pattern(Option('h', None, True), Option('f:', 'file=', 'f.txt'))
    assert Pattern(parse='-h --file f.txt arg', options=o, arguments=a) == \
               Pattern(Option('h', None, True), Option('f:', 'file=', 'f.txt'),
                       Argument(None, 'arg'))
    assert Pattern(parse='-h --file f.txt arg arg2', options=o, arguments=a) \
            == Pattern(Option('h', None, True), Option('f:', 'file=', 'f.txt'),
                       Argument(None, 'arg'), Argument(None, 'arg2'))

    assert Pattern(parse='[ -h ]', options=o) == \
               Pattern(Brackets(Option('h', None, True)))
    assert Pattern(parse='[ arg ... ]', options=o) == \
               Pattern(Brackets(Argument(None, 'arg'), Ellipsis))
    assert Pattern(parse='[ -h | -v ]', options=o) == \
               Pattern(Brackets(Option('h', None, True), VerticalBar,
                        Option('v', 'verbose', True)))
    assert Pattern(parse='( -h | -v [ --file f.txt ] )', options=o) == \
               Pattern(Parens(Option('h', None, True), VerticalBar,
                        Option('v', 'verbose', True),
                        Brackets(Option('f:', 'file=', 'f.txt'))))


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
