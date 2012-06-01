from __future__ import with_statement
from docopt import (Option, docopt, parse, Argument, Either, split_either,
                    Required, Optional, AnyOptions, pattern, OneOrMore,
                    parse_doc_options, option, Options, Arguments, DocoptExit,
                    GreedyEither, matching_paren, DocoptError, printable_usage,
                    formal_usage
                   )
from pytest import raises


def test_pattern_flat():
    assert Required(OneOrMore(Argument('N')),
                    Option('a'), Argument('M')).flat == \
                            [Argument('N'), Option('a'), Argument('M')]


def test_split():
    a = [1, 2, '|', 3, '|', 4, 5]
    assert split_either(a, '|') == [[1, 2], [3], [4, 5]]
    a = ['|', 3, '|']
    assert split_either(a, '|') == [[], [3], []]
    a = [1, '[', 2, '|', 3, ']', '|', 4, 5]
    assert split_either(a, '|') == [[1, '[', 2, '|', 3, ']'], [4, 5]]
    a = [1, '(', 2, '|', '[', 3, '|', 4, ']', ')', '|', 5]
    assert split_either(a, '|') == \
        [[1, '(', 2, '|', '[', 3, '|', 4, ']', ')'], [5]]


def test_matching_paren():
    assert matching_paren(['[', ']']) == 1
    assert matching_paren(['[', ']', '[', ']']) == 1
    assert matching_paren(['[', '[', ']', ']']) == 3
    with raises(DocoptError):
        matching_paren(['[', '[', ']'])
    with raises(DocoptError):
        docopt('Usage: prog [a [b]')
    #with raises(DocoptError):  # nice to have but minor
    #    docopt('Usage: prog [a [b] ] ]')


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
               Option('h:', None, '2')
    assert option('-h TOPIC  Descripton... [default: topic-1]') == \
               Option('h:', None, 'topic-1')
    assert option('--help=TOPIC  ... [default: 3.14]') == \
               Option(None, 'help=', '3.14')
    assert option('-h, --help=DIR  ... [default: ./]') == \
               Option('h:', 'help=', "./")
    assert option('-h TOPIC  Descripton... [dEfAuLt: 2]') == \
               Option('h:', None, '2')


def test_option_name():
    assert Option('h').name == 'h'
    assert Option('h', 'help').name == 'help'
    assert Option('h:', 'help=').name == 'help'
    assert Option('h', 'help-me').name == 'help_me'
    assert Option('2', '2-times').name == '__times'


def test_docopt():
    doc = '''Usage: prog [-v] a

    -v  Be verbose.'''
    assert docopt(doc, 'arg') == (Options(v=False), Arguments(a='arg'))
    assert docopt(doc, '-v arg') == (Options(v=True), Arguments(a='arg'))


def test_any_options():
    doc = '''Usage: prog [options] a

    -q  Be quiet
    -v  Be verbose.'''
    assert docopt(doc, 'arg') == (Options(v=False, q=False), Arguments(a='arg'))
    assert docopt(doc, '-v arg') == (Options(v=True, q=False), Arguments(a='arg'))
    assert docopt(doc, '-q arg') == (Options(v=False, q=True), Arguments(a='arg'))


def test_parse_doc_options():
    doc = '''-h, --help  Print help message.
    -o FILE     Output file.
    --verbose   Verbose mode.'''
    assert parse_doc_options(doc) == [Option('h', 'help'),
                                      Option('o:'),
                                      Option(None, 'verbose')]


def test_printable_and_formal_usage():
    doc = """
    Usage: prog [-hv] ARG
           prog N M

    prog is a program."""
    assert printable_usage(doc) == "Usage: prog [-hv] ARG\n           prog N M"
    assert formal_usage(printable_usage(doc)) == "[-hv] ARG | N M"
    assert printable_usage('uSaGe: prog ARG\n\t \t\n bla') == "uSaGe: prog ARG"


def test_parse():
    o = [Option('h'), Option('v', 'verbose'), Option('f:', 'file=')]
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
    assert parse('-h arg -- -v', options=o) == [Option('h', None, True),
                                                Argument(None, 'arg'),
                                                Argument(None, '-v')]
def test_pattern():
    o = [Option('h'), Option('v', 'verbose'), Option('f:', 'file=')]
    assert pattern('[ -h ]', options=o) == \
               Required(Optional(Option('h', None, True)))
    assert pattern('[ ARG ... ]', options=o) == \
               Required(Optional(OneOrMore(Argument('ARG'))))
    assert pattern('[ -h | -v ]', options=o) == \
               Required(Optional(Either(Option('h', None, True),
                                Option('v', 'verbose', True))))
    assert pattern('( -h | -v [ --file f.txt ] )', options=o) == \
               Required(Required(
                   Either(Option('h', None, True),
                          Required(Option('v', 'verbose', True),
                                 Optional(Option('f:', 'file=', 'f.txt'))))))
    assert pattern('(-h|-v[--file=f.txt]N...)', options=o) == \
               Required(Required(Either(Option('h', None, True),
                              Required(Option('v', 'verbose', True),
                                     Optional(Option('f:', 'file=', 'f.txt')),
                                     OneOrMore(Argument('N'))))))
    assert pattern('(N [M | (K | L)] | O P)') == \
               Required(Required(Either(
                   Required(Argument('N'),
                            Optional(Either(Argument('M'),
                                            Required(Either(Argument('K'),
                                                            Argument('L')))))),
                   Required(Argument('O'), Argument('P')))))
    assert pattern('[ -h ] [N]', options=o) == \
               Required(Optional(Option('h', None, True)),
                        Optional(Argument('N')))
    assert pattern('[options]') == Required(Optional(AnyOptions()))
    assert pattern('[options] A', options=o) == Required(
                Optional(AnyOptions()),
                Argument('A'))
    assert pattern('-v [options]', options=o) == Required(
                Option('v', 'verbose', True),
                Optional(AnyOptions()))


def test_option_match():
    assert Option('a').match([Option('a')]) == (True, [], [])
    assert Option('a').match([Option('x')]) == (False, [Option('x')], [])
    assert Option('a').match([Argument('N')]) == (False, [Argument('N')], [])
    assert Option('a').match([Option('x'), Option('a'), Argument('N')]) == \
            (True, [Option('x'), Argument('N')], [])
    assert Option('a', None, False).match([Option('a', None, False)]) == \
            (True, [], [])


def test_argument_match():
    assert Argument('N').match([Argument(None, 9)]) == (
            True, [], [Argument('N', 9)])
    assert Argument('N').match([Option('x')]) == (False, [Option('x')], [])
    assert Argument('N').match([Option('x'), Option('a'), Argument(None, 5)]) \
            == (True, [Option('x'), Option('a')], [Argument('N', 5)])
    assert Argument('N').match([Argument(None, 9), Argument(None, 0)]) == (
            True, [Argument(None, 0)], [Argument('N', 9)])


def test_brackets_match():
    assert Optional(Option('a')).match([Option('a')]) == (True, [], [])
    assert Optional(Option('a')).match([]) == (True, [], [])
    assert Optional(Option('a')).match([Option('x')]) == (
            True, [Option('x')], [])
    assert Optional(Option('a'), Option('b')).match([Option('a')]) == (
            True, [], [])
    assert Optional(Option('a'), Option('b')).match([Option('b')]) == (
            True, [], [])
    assert Optional(Option('a'), Option('b')).match([Option('x')]) == (
            True, [Option('x')], [])
    assert Optional(Argument('N')).match([Argument(None, 9)]) == (
            True, [], [Argument('N', 9)])


def test_parens_match():
    assert Required(Option('a')).match([Option('a')]) == (True, [], [])
    assert Required(Option('a')).match([]) == (False, [], [])
    assert Required(Option('a')).match([Option('x')]) == (
            False, [Option('x')], [])
    assert Required(Option('a'), Option('b')).match([Option('a')]) == (
            False, [Option('a')], [])
    assert Optional(Option('a'), Option('b')).match(
            [Option('b'), Option('x'), Option('a')]) == (
                    True, [Option('x')], [])


def test_either_match():
    assert Either(Option('a'), Option('b')).match(
            [Option('a')]) == (True, [], [])
    assert Either(Option('a'), Option('b')).match(
            [Option('a'), Option('b')]) == (True, [Option('b')], [])
    assert Either(Option('a'), Option('b')).match(
            [Option('x')]) == (False, [Option('x')], [])
    assert Either(Option('a'), Option('b'), Option('c')).match(
            [Option('x'), Option('b')]) == (True, [Option('x')], [])


def test_one_or_more_match():
    assert OneOrMore(Argument('N')).match([Argument(None, 9)]) == (
            True, [], [Argument('N', 9)])
    assert OneOrMore(Argument('N')).match([]) == (False, [], [])
    assert OneOrMore(Argument('N')).match([Option('x')]) == \
            (False, [Option('x')], [])
    assert OneOrMore(Argument('N')).match(
            [Argument(None, 9), Argument(None, 8)]) == (
                    True, [], [Argument('N', 9), Argument('N', 8)])
    assert OneOrMore(Argument('N')).match(
            [Argument(None, 9), Option('x'), Argument(None, 8)]) == (
                    True, [Option('x')], [Argument('N', 9), Argument('N', 8)])
    assert OneOrMore(Option('a')).match(
            [Option('a'), Argument(None, 8), Option('a')]) == (
                    True, [Argument(None, 8)], [])
    assert OneOrMore(Option('a')).match([Argument(None, 8), Option('x')]) == (
                    False, [Argument(None, 8), Option('x')], [])
#   NOTE, Option is greedy, nothing to match second time
#   assert OneOrMore(Required(Option('a'), Argument('N'))).match(
#           [Option('a'), Argument(None, 1), Option('x'),
#            Option('a'), Argument(None, 2)]) == \
#                    (True, [Option('x')], [Argument('N', 1), Argument('N', 2)])
    assert OneOrMore(Optional(Argument('N'))).match([Argument(None, 9)])
#                   (True, [], [Argument('N', 9)])


def test_list_argutent_match():
    assert Required(Argument('N'), Argument('N')).fix().match(
            [Argument(None, 1), Argument(None, 2)]) == \
                    (True, [], [Argument('N', [1, 2])])
    assert OneOrMore(Argument('N')).fix().match(
            [Argument(None, 1), Argument(None, 2), Argument(None, 3)]) == \
                    (True, [], [Argument('N', [1, 2, 3])])
    assert Required(Argument('N'), OneOrMore(Argument('N'))).fix().match(
            [Argument(None, 1), Argument(None, 2), Argument(None, 3)]) == \
                    (True, [], [Argument('N', [1, 2, 3])])
    assert Required(Argument('N'), Required(Argument('N'))).fix().match(
            [Argument(None, 1), Argument(None, 2)]) == \
                    (True, [], [Argument('N', [1, 2])])


def test_basic_pattern_matching():
    # ( -a N [ -x Z ] )
    pattern = Required(Option('a'), Argument('N'),
                       Optional(Option('x'), Argument('Z')))
    # -a N
    assert pattern.match([Option('a'), Argument(None, 9)]) == (
            True, [], [Argument('N', 9)])
    # -a -x N Z
    assert pattern.match([Option('a'), Option('x'),
                          Argument(None, 9), Argument(None, 5)]) == (
                                True, [], [Argument('N', 9), Argument('Z', 5)])
    # -x N Z  # BZZ!
    assert pattern.match([Option('x'),
                          Argument(None, 9),
                          Argument(None, 5)]) == (
                                False, [Option('x'),
                                        Argument(None, 9),
                                        Argument(None, 5)], [])

def test_pattern_any_option():
    pattern = AnyOptions()
    assert pattern.match([Option('a')]) == (True, [], [])
    assert pattern.match([Option('b')]) == (True, [], [])
    assert pattern.match([Option('l', 'long')]) == (True, [], [])
    assert pattern.match([Option(None, 'long')]) == (True, [], [])
    assert pattern.match([Option('a'), Option('b')]) == (True, [], [])
    assert pattern.match([Option('a'), Option(None, 'long')]) == (True, [], [])
    assert not pattern.match([Argument('N')])[0]


def test_pattern_either():
    assert Option('a').either == Either(Required(Option('a')))
    assert Argument('a').either == Either(Required(Argument('a')))
    assert Required(Either(Option('a'), Option('b')), Option('c')).either == \
            Either(Required(Option('a'), Option('c')),
                   Required(Option('b'), Option('c')))
    assert Optional(Option('a'), Either(Option('b'), Option('c'))).either == \
            Either(Required(Option('b'), Option('a')),
                   Required(Option('c'), Option('a')))
    assert Either(Option('x'), Either(Option('y'), Option('z'))).either == \
            Either(Required(Option('x')),
                   Required(Option('y')),
                   Required(Option('z')))
    assert OneOrMore(Argument('n'), Argument('m')).either == \
            Either(Required(Argument('n'), Argument('m'),
                            Argument('n'), Argument('m')))


def test_pattern_fix_list_arguments():
    assert Option('a').fix_list_arguments() == Option('a')
    assert Argument('n', None).fix_list_arguments() == Argument('n', None)
    assert Required(Argument('n'), Argument('n')).fix_list_arguments() == \
            Required(Argument('n', []), Argument('n', []))
    assert GreedyEither(Argument('N'),
                        OneOrMore(Argument('N'))).fix() == \
            GreedyEither(Argument('N', []),
                         OneOrMore(Argument('N', [])))


def test_greedy_either():
    assert GreedyEither(Argument('M'),
                        Required(Argument('N'), Argument('M'))).match(
                                   [Argument(None, 1), Argument(None, 2)]) == \
            (True, [], [Argument('N', 1), Argument('M', 2)])


def test_set():
    assert Argument('n') == Argument('n')
    assert set([Argument('n'), Argument('n')]) == set([Argument('n')])


def test_pattern_fix_identities_1():
    pattern = Required(Argument('n'), Argument('n'))
    assert pattern.children[0] == pattern.children[1]
    assert pattern.children[0] is not pattern.children[1]
    pattern.fix_identities()
    assert pattern.children[0] is pattern.children[1]


def test_pattern_fix_identities_2():
    pattern = Required(Optional(Argument('x'), Argument('n')), Argument('n'))
    assert pattern.children[0].children[1] == pattern.children[1]
    assert pattern.children[0].children[1] is not pattern.children[1]
    pattern.fix_identities()
    assert pattern.children[0].children[1] is pattern.children[1]


def test_long_options_error_handling():
    with raises(DocoptError):
        docopt('Usage: prog --non-existent')
    with raises(DocoptExit):
        docopt('Usage: prog', '--non-existent')
    with raises(DocoptError):
        docopt('Usage: prog --ver\n\n--version\n--verbose')
    with raises(DocoptExit):
        docopt('''Usage: prog [--version --verbose]\n\n
                  --version\n--verbose''', '--ver')
    with raises(DocoptError):
        docopt('Usage: prog --long\n\n--long ARG')
    with raises(DocoptExit):
        docopt('Usage: prog --long ARG\n\n--long ARG', '--long')
    with raises(DocoptError):
        docopt('Usage: prog --long=arg\n\n--long')
    with raises(DocoptExit):
        docopt('Usage: prog --long\n\n--long', '--long=arg')


def test_short_options_error_handling():
    with raises(DocoptError):
        docopt('Usage: prog -x\n\n-x  this\n-x  that')

    with raises(DocoptError):
        docopt('Usage: prog -x')
    with raises(DocoptExit):
        docopt('Usage: prog', '-x')

    with raises(DocoptError):
        docopt('Usage: prog -o\n\n-o ARG')
    with raises(DocoptExit):
        docopt('Usage: prog -o ARG\n\n-o ARG', '-o')

def test_empty_pattern():
    # See https://github.com/halst/docopt/issues/9
    doc = '''usage: prog'''
    docopt(doc, '')
