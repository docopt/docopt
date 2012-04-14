from docopt import (Option, Options, docopt, Pattern, Argument, VerticalBar,
        Required, NotRequired)


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
               Pattern(NotRequired(Option('h', None, True)))
    assert Pattern(parse='[ arg ... ]', options=o) == \
               Pattern(NotRequired(Argument(None, 'arg'), Ellipsis))
    assert Pattern(parse='[ -h | -v ]', options=o) == \
               Pattern(NotRequired(Option('h', None, True), VerticalBar,
                        Option('v', 'verbose', True)))
    assert Pattern(parse='( -h | -v [ --file f.txt ] )', options=o) == \
               Pattern(Required(Option('h', None, True), VerticalBar,
                        Option('v', 'verbose', True),
                        NotRequired(Option('f:', 'file=', 'f.txt'))))

#   assert Pattern(parse='-h', options=o).match('-h')
#   assert Pattern(parse='( -h )', options=o).match('-h')
#   assert not Pattern(parse='-h', options=o).match('-v')


def test_option_match():
    matched, left = Option('a').match([Option('a')])
    assert matched == [Option('a')]
    assert left == []

    matched, left = Option('b').match([Option('a')])
    assert matched == False
    assert left == [Option('a')]

    matched, left = Option('b').match([])
    assert matched == False
    assert left == []

    matched, left = Option('a').match([Argument('A')])
    assert matched == False
    assert left == [Argument('A')]


def test_not_required_match():
    matched, left = NotRequired(Option('a')).match([])
    assert matched == []
    assert left == []

    matched, left = NotRequired(Option('a')).match([Option('a')])
    assert matched == [Option('a')]
    assert left == []

    matched, left = NotRequired(Option('b')).match([Option('a')])
    assert matched == []
    assert left == [Option('a')]

    matched, left = NotRequired(Option('a'), Option('b')).match([Option('b')])
    assert matched == [Option('b')]
    assert left == []

    matched, left = NotRequired(Option('a'), Option('b')).match([Option('c')])
    assert matched == []
    assert left == [Option('c')]

    matched, left = NotRequired(Option('a'), Option('b')).match(
            [Option('b'), Option('a')])
    assert matched == [Option('b'), Option('a')]
    assert left == []

    matched, left = NotRequired(Option('a'), Option('b')).match(
            [Option('b'), Option('c'), Option('a')])
    assert matched == [Option('b'), Option('a')]
    assert left == [Option('c')]


def test_required_match():
    matched, left = Required(Option('a')).match([])
    assert matched is False
    assert left == []

    matched, left = Required(Option('a')).match([Option('a')])
    assert matched == [Option('a')]
    assert left == []

    matched, left = Required(Option('b')).match([Option('a')])
    assert matched is False
    assert left == [Option('a')]

    matched, left = Required(Option('b'), Option('a')).match(
            [Option('a'), Option('c'), Option('b')])
    assert matched == [Option('a'), Option('b')]
    assert left == [Option('c')]


def test_required_and_not_required_match():
    matched, left = Required(Option('a'), NotRequired(Option('b'))).match(
            [Option('a'), Option('b')])
    assert matched == [Option('a'), Option('b')]
    assert left == []
    # (-a [-b])
    matched, left = Required(Option('a'), NotRequired(Option('b'))).match(
            [Option('a')])
    assert matched == [Option('a')]
    assert left == []

#   matched, left = Required(Option('a'), NotRequired(Option('b'))).match(
#           [Option('b')])
#   assert matched is False
#   assert left == []


#def test_not_required_match():
#    assert NotRequired(
#            Option('a', None, False)).match(Option('a', None, True)) == \
#             Option('a', None, True)
#def test_not_required():
#    assert NotRequired(Option('a')).
