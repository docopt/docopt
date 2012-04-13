from docopt import Option, Options, docopt, Pattern, Argument, Token


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
    assert Pattern(parse='-h --file f.txt arg arg2', options=o, arguments=a) == \
               Pattern(Option('h', None, True), Option('f:', 'file=', 'f.txt'),
                       Argument(None, 'arg'), Argument(None, 'arg2'))

    assert Pattern(parse='[ -h ]', options=o) == \
               Pattern(Token('['), Option('h', None, True), Token(']'))
#   assert Pattern(parse='[ -h ]', options=o) == \
#              Pattern([Option('h', None, True)])
