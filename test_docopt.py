from __future__ import with_statement
from docopt import (docopt, DocoptExit, DocoptError,
                    Option, Argument, Command,
                    Required, Optional, Either, OneOrMore, AnyOptions,
                    parse_args, parse_pattern,
                    parse_doc_options, option, printable_usage, formal_usage
                   )
from pytest import raises


def test_pattern_flat():
    assert Required(OneOrMore(Argument('N')),
                    Option('a'), Argument('M')).flat == \
                            [Argument('N'), Option('a'), Argument('M')]


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
    assert Option('h').name == '-h'
    assert Option('h', 'help').name == '--help'
    assert Option('h:', 'help=').name == '--help'
    assert Option('h', 'help-me').name == '--help-me'
    assert Option('2', '2-times').name == '--2-times'


def test_docopt():
    doc = '''Usage: prog [-v] A

    -v  Be verbose.'''
    assert docopt(doc, 'arg') == {'-v': False, 'A': 'arg'}
    assert docopt(doc, '-v arg') == {'-v': True, 'A': 'arg'}


def test_any_options():
    doc = '''Usage: prog [options] A

    -q  Be quiet
    -v  Be verbose.'''
    assert docopt(doc, 'arg') == {'A': 'arg', '-v': False, '-q': False}
    assert docopt(doc, '-v arg') == {'A': 'arg', '-v': True, '-q': False}
    assert docopt(doc, '-q arg') == {'A': 'arg', '-v': False, '-q': True}


def test_commands():
    assert docopt('Usage: prog add', 'add') == {'add': True}
    assert docopt('Usage: prog [add]', '') == {'add': False}
    assert docopt('Usage: prog [add]', 'add') == {'add': True}
    assert docopt('Usage: prog (add|rm)', 'add') == {'add': True, 'rm': False}
    assert docopt('Usage: prog (add|rm)', 'rm') == {'add': False, 'rm': True}
    assert docopt('Usage: prog a b', 'a b') == {'a': True, 'b': True}
    with raises(DocoptExit):
        assert docopt('Usage: prog a b', 'b a')


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


def test_parse_args():
    o = [Option('h'), Option('v', 'verbose'), Option('f:', 'file=')]
    assert parse_args('', options=o) == []
    assert parse_args('-h', options=o) == [Option('h', None, True)]
    assert parse_args('-h --verbose', options=o) == \
            [Option('h', None, True), Option('v', 'verbose', True)]
    assert parse_args('-h --file f.txt', options=o) == \
            [Option('h', None, True), Option('f:', 'file=', 'f.txt')]
    assert parse_args('-h --file f.txt arg', options=o) == \
            [Option('h', None, True),
             Option('f:', 'file=', 'f.txt'),
             Argument(None, 'arg')]
    assert parse_args('-h --file f.txt arg arg2', options=o) == \
            [Option('h', None, True),
             Option('f:', 'file=', 'f.txt'),
             Argument(None, 'arg'),
             Argument(None, 'arg2')]
    assert parse_args('-h arg -- -v', options=o) == \
            [Option('h', None, True),
             Argument(None, 'arg'),
             Argument(None, '-v')]


def test_parse_pattern():
    o = [Option('h'), Option('v', 'verbose'), Option('f:', 'file=')]
    assert parse_pattern('[ -h ]', options=o) == \
               Required(Optional(Option('h', None, True)))
    assert parse_pattern('[ ARG ... ]', options=o) == \
               Required(Optional(OneOrMore(Argument('ARG'))))
    assert parse_pattern('[ -h | -v ]', options=o) == \
               Required(Optional(Either(Option('h', None, True),
                                Option('v', 'verbose', True))))
    assert parse_pattern('( -h | -v [ --file f.txt ] )', options=o) == \
               Required(Required(
                   Either(Option('h', None, True),
                          Required(Option('v', 'verbose', True),
                                 Optional(Option('f:', 'file=', 'f.txt'))))))
    assert parse_pattern('(-h|-v[--file=f.txt]N...)', options=o) == \
               Required(Required(Either(Option('h', None, True),
                              Required(Option('v', 'verbose', True),
                                     Optional(Option('f:', 'file=', 'f.txt')),
                                     OneOrMore(Argument('N'))))))
    assert parse_pattern('(N [M | (K | L)] | O P)', options=[]) == \
               Required(Required(Either(
                   Required(Argument('N'),
                            Optional(Either(Argument('M'),
                                            Required(Either(Argument('K'),
                                                            Argument('L')))))),
                   Required(Argument('O'), Argument('P')))))
    assert parse_pattern('[ -h ] [N]', options=o) == \
               Required(Optional(Option('h', None, True)),
                        Optional(Argument('N')))
    assert parse_pattern('[options]', options=o) == Required(
                Optional(AnyOptions()))
    assert parse_pattern('[options] A', options=o) == Required(
                Optional(AnyOptions()),
                Argument('A'))
    assert parse_pattern('-v [options]', options=o) == Required(
                Option('v', 'verbose', True),
                Optional(AnyOptions()))

    assert parse_pattern('ADD', options=o) == Required(Argument('ADD'))
    assert parse_pattern('<add>', options=o) == Required(Argument('<add>'))
    assert parse_pattern('add', options=o) == Required(Command('add'))


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


def test_command_match():
    assert Command('c').match([Argument(None, 'c')]) == (
            True, [], [Command('c', True)])
    assert Command('c').match([Option('x')]) == (False, [Option('x')], [])
    assert Command('c').match([Option('x'), Option('a'),
                               Argument(None, 'c')]) == (
            True, [Option('x'), Option('a')], [Command('c', True)])
    assert Either(Command('add', False), Command('rm', False)).match(
            [Argument(None, 'rm')]) == (True, [], [Command('rm', True)])


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
    assert Either(Argument('M'),
                  Required(Argument('N'), Argument('M'))).match(
                                   [Argument(None, 1), Argument(None, 2)]) == \
            (True, [], [Argument('N', 1), Argument('M', 2)])


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
    assert OneOrMore(Optional(Argument('N'))).match([Argument(None, 9)]) == \
                    (True, [], [Argument('N', 9)])


def test_list_argument_match():
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
    assert AnyOptions().match([Option('a')]) == (True, [], [])
    assert AnyOptions().match([Option('b')]) == (True, [], [])
    assert AnyOptions().match([Option('l', 'long')]) == (True, [], [])
    assert AnyOptions().match([Option(None, 'long')]) == (True, [], [])
    assert AnyOptions().match([Option('a'), Option('b')]) == (True, [], [])
    assert AnyOptions().match([Option('a'),
                               Option(None, 'long')]) == (True, [], [])
    assert not AnyOptions().match([Argument('N')])[0]


def test_pattern_either():
    assert Option('a').either == Either(Required(Option('a')))
    assert Argument('A').either == Either(Required(Argument('A')))
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
    assert OneOrMore(Argument('N'), Argument('M')).either == \
            Either(Required(Argument('N'), Argument('M'),
                            Argument('N'), Argument('M')))


def test_pattern_fix_list_arguments():
    assert Option('a').fix_list_arguments() == Option('a')
    assert Argument('N', None).fix_list_arguments() == Argument('N', None)
    assert Required(Argument('N'), Argument('N')).fix_list_arguments() == \
            Required(Argument('N', []), Argument('N', []))
    assert Either(Argument('N'),
                        OneOrMore(Argument('N'))).fix() == \
           Either(Argument('N', []),
                        OneOrMore(Argument('N', [])))


def test_set():
    assert Argument('N') == Argument('N')
    assert set([Argument('N'), Argument('N')]) == set([Argument('N')])


def test_pattern_fix_identities_1():
    pattern = Required(Argument('N'), Argument('N'))
    assert pattern.children[0] == pattern.children[1]
    assert pattern.children[0] is not pattern.children[1]
    pattern.fix_identities()
    assert pattern.children[0] is pattern.children[1]


def test_pattern_fix_identities_2():
    pattern = Required(Optional(Argument('X'), Argument('N')), Argument('N'))
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
        docopt('Usage: prog --long=ARG\n\n--long')
    with raises(DocoptExit):
        docopt('Usage: prog --long\n\n--long', '--long=ARG')


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


def test_allow_double_underscore_in_pattern():
    docopt('usage: prog [-o] [--] <arg>\n\n-o',
           '-- -o') == {'-o': False, '<arg>': '-o'}


def test_allow_empty_pattern():
    docopt('usage: prog', '') == {}
