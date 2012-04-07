






from docopt import Option


def test_option_short_only():
    o = Option('-f')
    assert o.short == '-f'
    assert o.full == None
    assert o.name == 'f'
    assert o.argument_count == 0
    assert o.default == None


def test_option_full_only():
    o = Option('--foo')
    assert o.short == None
    assert o.full == '--foo'
    assert o.name == 'foo'
    assert o.argument_count == 0
    assert o.default == None


def test_option_short_and_full():
    o = Option('-f --foo')
    assert o.short == '-f'
    assert o.full == '--foo'
    assert o.name == 'foo'
    assert o.argument_count == 0
    assert o.default == None


def test_option_with_description():
    o = Option('-f --foo description goes here')
    assert o.short == '-f'
    assert o.full == '--foo'
    assert o.name == 'foo'
    assert o.argument_count == 0
    assert o.default == None


def test_option_short_with_1_argument():
    o = Option('-f=ARG')
    assert o.short == '-f'
    assert o.full == None
    assert o.name == 'f'
    assert o.argument_count == 1
    assert o.default == None


def test_option_full_with_1_argument():
    o = Option('--foo=ARG')
    assert o.short == None
    assert o.full == '--foo'
    assert o.name == 'foo'
    assert o.argument_count == 1
    assert o.default == None


def test_option_short_and_full_with_1_argument():
    #assert (Option(parse='-f=ARG  --foo=ARG') ==
    #        Option('-f', '--foo', 'foo', 1, None))

    o = Option('-f=ARG  --foo=ARG')
    assert o.short == '-f'
    assert o.full == '--foo'
    assert o.name == 'foo'
    assert o.argument_count == 1
    assert o.default == None


def test_option_with_1_argument_and_description():
    o = Option('-f=ARG --foo=ARG description goes here')
    assert o.short == '-f'
    assert o.full == '--foo'
    assert o.name == 'foo'
    assert o.argument_count == 1
    assert o.default == None
#def test_option_long_name():
