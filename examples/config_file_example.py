"""Usage:
  quick_example.py tcp [<host>] [--force] [--timeout=<seconds>]
  quick_example.py serial <port> [--baud=<rate>] [--timeout=<seconds>]
  quick_example.py -h | --help | --version

"""
from collections import ChainMap
from docopt import docopt


def load_json_config():
    import json
    # Pretend that we load the following JSON file:
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

    # By using `allow_no_value=True` we are allowed to
    # write `--force` instead of `--force=true` below.
    config = ConfigParser(allow_no_value=True)

    # Pretend that we load the following INI file:
    source = '''
        [default-arguments]
        --force
        --baud=19200
        <host>=localhost
    '''

    # ConfigParser requires a file-like object and
    # no leading whitespace.
    config_file = StringIO('\n'.join(source.split()))
    config.readfp(config_file)

    # ConfigParsers sets keys which have no value
    # (like `--force` above) to `None`. Thus we
    # need to substitute all `None` with `True`.
    return dict((key, True if value is None else value)
                for key, value in config.items('default-arguments'))


if __name__ == '__main__':
    json_config = load_json_config()
    ini_config = load_ini_config()
    arguments = docopt(__doc__, version='0.1.1rc', hide_unset=True)

    # Arguments take priority over INI, INI takes priority over JSON:
    result = ChainMap(arguments, ini_config, json_config)

    from pprint import pprint
    print('\nJSON config:')
    pprint(json_config)
    print('\nINI config:')
    pprint(ini_config)
    print('\nResult:')
    pprint(result)
