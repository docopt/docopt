from docopt import (Argument, Command, Either, OneOrMore, Option, Required,
                    docopt)


def test_repeated_options_are_not_duplicated_by_alternatives():
    usage = '''Usage:
      prog update [--table=<tables>...]
      prog update schema [--table=<tables>...]
    '''
    assert docopt(usage, 'update schema --table=1 --table=2') == {
        'update': True, 'schema': True, '--table': ['1', '2']}


def test_failed_alternative_does_not_change_collected_values():
    pattern = Required(
        Option('-t', None, 1, []),
        Either(Required(Option('-t', None, 1, []), Command('missing')),
               Option('-t', None, 1, [])))
    left = [Option('-t', None, 1, 'one'), Option('-t', None, 1, 'two')]
    matched, remaining, collected = pattern.match(left)
    assert matched
    assert remaining == []
    assert collected == [Option('-t', None, 1, ['one', 'two'])]
    assert left == [Option('-t', None, 1, 'one'), Option('-t', None, 1, 'two')]


def test_failed_alternative_does_not_change_repeated_command_count():
    pattern = Required(
        Command('go', 0),
        Either(Required(Command('go', 0), Command('missing')),
               Command('go', 0)))
    matched, remaining, collected = pattern.match([Argument(None, 'go'),
                                                  Argument(None, 'go')])
    assert matched
    assert remaining == []
    assert collected == [Command('go', 2)]


def test_one_or_more_does_not_mutate_input_or_collected_arguments():
    pattern = OneOrMore(Option('-t', None, 1, []))
    left = [Option('-t', None, 1, 'one'), Option('-t', None, 1, 'two')]
    collected = [Option('-t', None, 1, ['zero'])]
    result = pattern.match(left, collected)
    assert result == (True, [], [Option('-t', None, 1, ['zero', 'one', 'two'])])
    assert collected == [Option('-t', None, 1, ['zero'])]
    assert left == [Option('-t', None, 1, 'one'), Option('-t', None, 1, 'two')]
