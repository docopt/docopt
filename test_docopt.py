from docopt import (Option, Namespace, docopt, parse, Argument, VerticalBar,
                    Parens, Brackets, pattern, OneOrMore, parse_doc_options,
                    parse_doc_usage, option, Options, Arguments)


def test_option():
    assert option('-h') == Option('h', None)
    assert option('--help') == Option(None, 'help')
    assert option('-h --help') == Option('h', 'help')
    assert option('-h, --help') == Option('h', 'help')

    assert option('-h TOPIC') == Option('h:', None)
    assert option('--help TOPIC') == Option(None, 'help=')
    assert option('-h TOPIC --help TOPIC') == Option('h:', 'help=')
    assert option('-h TOPIC, --help TOPIC') == Option('h:', 'help=')
    assert option('-h TOPIC, --help=TOPIC') == Option('h:', 'help=')

    assert option('-h  Description...') == Option('h', None)
    assert option('-h --help  Description...') == Option('h', 'help')
    assert option('-h TOPIC  Description...') == Option('h:', None)

    assert option('    -h') == Option('h', None)

    assert option('-h TOPIC  Descripton... [default: 2]') == \
               Option('h:', None, 2)
    assert option('-h TOPIC  Descripton... [default: topic-1]') == \
               Option('h:', None, 'topic-1')
    assert option('--help=TOPIC  ... [default: 3.14]') == \
               Option(None, 'help=', 3.14)
    assert option('-h, --help=DIR  ... [default: "./"]') == \
               Option('h:', 'help=', "./")


def test_option_name():
    assert Option('h').name == 'h'
    assert Option('h', 'help').name == 'help'
    assert Option('h:', 'help=').name == 'help'
    assert Option('h', 'help-me').name == 'help_me'
    assert Option('2', '2-times').name == '__times'


def test_docopt():
#   assert docopt('\n-v  Be verbose.', ['-v']) == (
#           Options(v=True), Arguments())
#   assert docopt('-v  Be verbose.', ['-v']) == (
#           Options(v=True), Arguments())
    doc = '''Usage: prog -v a

    -v  Be verbose.'''
    assert docopt(doc, ['arg']) == (
            Options(v=False), Arguments(a='arg'))


def test_parse_doc_options():
    doc = """-h, --help  Print help message.
    -o FILE     Output file.
    --verbose   Verbose mode."""
    assert parse_doc_options(doc) == [Option('h', 'help'),
                                      Option('o:'),
                                      Option(None, 'verbose')]


#def test_parse_doc_usage():
#    assert parse_doc_usage('usage: prog ARG') == [Parens(Argument('ARG'))]
#    doc = """
#    Usage: prog [-hv]
#                 ARG
#           prog N M
#
#    prog is a program.
#
#    -h
#    -v
#
#    """
#    assert parse_doc_usage(doc, options=parse_doc_options(doc)) == [
#            Parens(Brackets(Option('h', None, True),
#                            Option('v', None, True)), Argument('ARG')),
#            Parens(Argument('N'), Argument('M'))]


def test_parse_doc_usage():
    assert parse_doc_usage('usage: prog ARG') == ['ARG']
    doc = """
    Usage: prog [-hv] ARG
           prog N M

    prog is a program.

    -h
    -v

    """
    assert parse_doc_usage(doc) == ['[-hv] ARG', 'N M']


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
             Argument('arg')]
    assert parse('-h --file f.txt arg arg2', options=o) == \
            [Option('h', None, True),
             Option('f:', 'file=', 'f.txt'),
             Argument('arg'),
             Argument('arg2')]

    assert pattern('[ -h ]', options=o) == \
               [Brackets(Option('h', None, True))]
    assert pattern('[ ARG ... ]', options=o) == \
               [Brackets(OneOrMore(Argument('ARG')))]
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
                       OneOrMore(Argument('N')))]


def test_option_match():
    assert Option('a').match([Option('a')]) == (True, [])
    assert Option('a').match([Option('x')]) == (False, [Option('x')])
    assert Option('a').match([Argument('N')]) == (False, [Argument('N')])
    assert Option('a').match([Option('x'), Option('a'), Argument('N')]) == \
            (True, [Option('x'), Argument('N')])
    assert Option('a', None, False).match([Option('a', None, False)]) == \
            (True, [])


def test_argument_match():
    assert Argument('N').match([Argument(9)]) == (True, [])
    assert Argument('N').match([Option('x')]) == (False, [Option('x')])
    assert Argument('N').match([Option('x'), Option('a'), Argument('N')]) == \
            (True, [Option('x'), Option('a')])
    assert Argument('N').match([Argument(9), Argument(0)]) == \
            (True, [Argument(0)])


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
    assert OneOrMore(Argument('N')).match([Argument(9)]) == (True, [])
    assert OneOrMore(Argument('N')).match([]) == (False, [])
    assert OneOrMore(Argument('N')).match([Option('x')]) == \
            (False, [Option('x')])
    assert OneOrMore(Argument('N')).match(
            [Argument(9), Argument(8)]) == (True, [])
    assert OneOrMore(Argument('N')).match(
            [Argument(9), Option('x'), Argument(8)]) == \
                    (True, [Option('x')])
    assert OneOrMore(Option('a')).match(
            [Option('a'), Argument(8), Option('a')]) == \
                    (True, [Argument(8)])
    assert OneOrMore(Option('a')).match([Argument(8), Option('x')]) == \
                    (False, [Argument(8), Option('x')])
    assert OneOrMore(Parens(Option('a'), Argument('N'))).match(
            [Option('a'), Argument(1), Option('x'),
             Option('a'), Argument(2)]) == (True, [Option('x')])


def test_basic_pattern_matching():
    # ( -a N [ -x Z ] )
    pattern = Parens(Option('a'), Argument('N'),
                     Brackets(Option('x'), Argument('Z')))
    # -a N
    assert pattern.match([Option('a'), Argument(9)]) == (True, [])
    # -a -x N Z
    assert pattern.match([Option('a'), Option('x'),
                          Argument(9), Argument(5)]) == (True, [])
    # -x N Z  # BZZ!
    assert pattern.match([Option('x'),
                          Argument(9), Argument(5)]) == (False, [])
