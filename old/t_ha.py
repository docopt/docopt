'''This docstring is not a docstring, but a part of the test.
Usage: prog-name [options] [arguments]
    -h, --help    Help.
    -v --verbose  Be verbose.
                  Very verbose.
    -o, --out=<file>
                  Output.
                  [default: file.txt]
    -r            Recursive.
    -i=file       Input.
    --number=9    Specify number.'''


def test__parse_help_entry():
    from human_arguments import _parse_single_description as pd
    assert pd('-v, --verbose') == ('v', 'verbose', False, False, None)
    assert pd('-v --verbose  ') == ('v', 'verbose', False, False, None)
    assert pd('--verbose  ') == (None, 'verbose', False, False, None)
    assert pd('-v  ') == ('v', None, False, False, None)
    assert pd('--verbose=foo  ') == (None, 'verbose', True, False, None)
    assert pd('-v, --verbose=foo  ') == ('v', 'verbose', True, False, None)
    assert pd('-v=foo  ') == ('v', None, True, False, None)
    assert pd('--ver=foo bar[default: 123]') == (None, 'ver', True, True, 123)
    assert pd('-v --ver=foo default: abc ') == ('v', 'ver', True, True, "abc")
    assert pd('-v=foo (default: 3.14e-2)') == ('v', None, True, True, 3.14e-2)
    assert pd('-v=foo (Default: {1:2})') == ('v', None, True, True, {1:2})


def test__variabalize():
    from human_arguments import _variabalize as va
    assert va('oh, hai') == 'oh__hai'
    assert va('oh-my') == 'oh_my'
    assert va('get 1 cure') == 'get_1_cure'
    assert va('%$@ he said') == '____he_said'


def test__normalize_argv():
    from human_arguments import _normalize_args as na
    assert na(['ls', '-al']) == ['ls', '-a', '-l']
    assert na(['foo', '--baz', '-o=bar']) == ['foo', '--baz', '-o', 'bar']
    assert na(['bar', '-baz=file']) == ['bar', '-b', '-a', '-z', 'file']


def test__parse_description():
    from human_arguments import _parse_description
    pd = _parse_description(__doc__)
    assert pd[0].short == 'h'
    assert pd[0].full == 'help'
    assert pd[1].short == 'v'
    assert pd[1].full == 'verbose'
    assert pd[2].short == 'o'
    assert pd[2].full == 'out'
    assert pd[3].short == 'r'
    assert pd[3].full == None
    assert pd[4].short == 'i'
    assert pd[4].full == None
    assert pd[5].short == None
    assert pd[5].full == 'number'


def test__split_opt_arg():
    from human_arguments import _parse_description
    from human_arguments import _split_options_and_arguments as soa
    pd = _parse_description(__doc__)
    assert soa(['ls', '-l'], pd) == (['-l'], [])
    assert soa(['ls', '-l', '.'], pd) == (['-l'], ['.'])
    assert soa(['foo', '-o=file'], pd) == (['-o', 'file'], [])
    assert soa(['foo', '-o', 'file'], pd) == (['-o', 'file'], [])
    assert soa(['foo', '-ao', 'file'], pd) == (['-a', '-o', 'file'], [])
    assert soa(['foo', '-r', 'file'], pd) == (['-r'], ['file'])
    assert soa(['foo', '--verbose', 'file'], pd) == (['--verbose'], ['file'])


def test__group_options():
    from human_arguments import _group_options as go
    assert go(['-v', '-o', 'file']) == [['-v'], ['-o', 'file']]
    assert go(['-v', '-i', 'f1', '-o', 'f2']) == [['-v'], ['-i', 'f1'], ['-o', 'f2']]


def test__parse_options():
    from human_arguments import _FormalOptionCollection
    from human_arguments import _parse_options as po
    pd = _FormalOptionCollection(__doc__)
    assert po(['-h', '-v', '-r'], pd) == {'help':True, 'verbose':True, 'r':True}
    assert po(['-o', 'file'], pd) == {'out':'file'}
    assert po(['-o', '3.14'], pd) == {'out':3.14}

#def test__parse_help():
#    parsed = _parse_help_string(__doc__)
#
#def test_parse_options():
#    sys_argv=['prog-name', '--verbose', '--mode=normal']
#    opt, arg = parse_options(__doc__, sys_argv)
#
#    assert opt.verbose == True
#    assert opt.mode == 'normal'
