"""Usage:
  quick_example.py tcp [<host>] [--force] [--timeout=<seconds>]
  quick_example.py serial <port> [--baud=<rate>] [--timeout=<seconds>]
  quick_example.py -h | --help | --version

"""
from docopt import docopt


def load_json_config():
    import json
    # Pretend that we load the following JSON string from a config file:
    source = '''
        {"--force": true,
         "--timeout": "10",
         "--baud": "9600"}
    '''
    return json.loads(source)


def load_ini_config():
    try:  # Python 2
        from ConfigParser import ConfigParser
        from StringIO import StringIO
    except ImportError:  # Python 3
        from configparser import ConfigParser
        from io import StringIO

    # Pretend that we load the following INI string from a config file:
    source = StringIO('[default-arguments]\n'
                      '--force\n'
                      '--baud=19200\n'
                      '<host>=localhost')

    # By using `allow_no_value=True` we are allowed to
    # write `--force` instead of `--force=true` above.
    config = ConfigParser(allow_no_value=True)
    config.readfp(source)

    # ConfigParsers sets keys which have no value
    # (like `--force` above) to `None`. Thus we
    # need to substitute all `None` with `True`.
    return dict((key, True if value is None else value)
                for key, value in config.items('default-arguments'))


def merge(dict_1, dict_2):
    """Merge two dictionaries.

    Values that evaluate to true take priority over falsy values.
    `dict_2` takes priority over `dict_1`.

    """
    return dict((str(key), dict_2.get(key) or dict_1.get(key))
                for key in set(dict_1) | set(dict_2))


if __name__ == '__main__':
    json_config = load_json_config()
    ini_config = load_ini_config()
    arguments = docopt(__doc__, version='0.1.1rc')

    # INI takes priority over JSON; arguments take priority overall.
    result = merge(json_config, merge(ini_config, arguments))

    from pprint import pprint
    print('\nJSON config:')
    pprint(json_config)
    print('\nINI config:')
    pprint(ini_config)
    print('\nResult:')
    pprint(result)
