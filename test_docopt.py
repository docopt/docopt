from docopt import Option, Options, parse_doc, docopt


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


def test_parse_doc():
    doc = """Usage program.py [options] arguments
    -h, --help  Print help message.
    -o FILE     Output file.
    --verbose   Verbose mode."""
    assert parse_doc(doc) == [Option('h', 'help'),
                              Option('o:'),
                              Option(None, 'verbose')]

def test_docopt():
    assert docopt('\n-h  Show help.', ['-h']) == (Options(h=True), [])
