# docopt – Create Beautiful Command-Line Interfaces

[![PyPI version](https://img.shields.io/pypi/v/docopt.svg)](https://pypi.python.org/pypi/docopt)
[![Python versions](https://img.shields.io/pypi/pyversions/docopt.svg)](https://pypi.python.org/pypi/docopt)
[![License](https://img.shields.io/pypi/l/docopt.svg)](https://github.com/docopt/docopt/blob/master/LICENSE)

Video introduction to **docopt**: [PyCon UK 2012: Create *beautiful* command-line interfaces with Python](http://youtu.be/pXhcPJK5cMc)

> **New in version 1.0.0 (2025)**
>
> - 🎉 **Production/Stable Release** - docopt is now officially stable!
> - 🐍 **Python 3.10+ Only** - Dropped Python 2.7 and 3.4-3.9 support
> - ✨ **Modernized Codebase** - Using modern Python idioms (f-strings, pathlib, etc.)
> - 🚀 **100% Backward Compatible** - No API changes for Python 3.10+ users
> 
> See [CHANGELOG.md](CHANGELOG.md) for full details.

---

## Philosophy

Isn't it awesome how `optparse` and `argparse` generate help messages based on your code?!

**Hell no!** You know what's awesome? It's when the option parser *is* generated based on the beautiful help message that you write yourself! This way you don't need to write this stupid repeatable parser-code, and instead can write only the help message—*the way you want it*.

**docopt** helps you create the most beautiful command-line interfaces *easily*:

```python
"""Naval Fate.

Usage:
  naval_fate.py ship new <name>...
  naval_fate.py ship <name> move <x> <y> [--speed=<kn>]
  naval_fate.py ship shoot <x> <y>
  naval_fate.py mine (set|remove) <x> <y> [--moored | --drifting]
  naval_fate.py (-h | --help)
  naval_fate.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --speed=<kn>  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.

"""
from docopt import docopt


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Naval Fate 2.0')
    print(arguments)
```

Beat that! The option parser is generated based on the docstring above that is passed to `docopt` function. `docopt` parses the usage pattern (`"Usage: ..."`) and option descriptions (lines starting with dash `"-"`) and ensures that the program invocation matches the usage pattern; it parses options, arguments and commands based on that. The basic idea is that *a good help message has all necessary information in it to make a parser*.

Also, [PEP 257](http://www.python.org/dev/peps/pep-0257/) recommends putting help message in the module docstrings.

## Installation

Use [pip](http://pip-installer.org):

```bash
pip install docopt
```

Alternatively, you can just drop `docopt.py` file into your project—it is self-contained.

**Requirements:**
- Python 3.10 or higher

**Legacy Python Support:**
- For Python 2.7 and 3.4-3.9, use `docopt==0.6.2`

## Testing

Run the test suite:

```bash
# Install development dependencies
pip install pytest

# Run tests
pytest

# Run tests with coverage
pytest --cov=docopt
```

## API

```python
from docopt import docopt
```

```python
docopt(doc, argv=None, help=True, version=None, options_first=False)
```

`docopt` takes 1 required and 4 optional arguments:

### Parameters

- **`doc`** (str, required): A help message that will be parsed to create the option parser. This could be a module docstring (`__doc__`) or any other string. Here is a quick example:

  ```python
  """Usage: my_program.py [-hso FILE] [--quiet | --verbose] [INPUT ...]

  -h --help    show this
  -s --sorted  sorted output
  -o FILE      specify output file [default: ./test.txt]
  --quiet      print less text
  --verbose    print more text

  """
  ```

- **`argv`** (list, optional): Argument vector to be parsed. By default `docopt` uses the argument vector passed to your program (`sys.argv[1:]`). You can supply a list of strings like `['--verbose', '-o', 'hai.txt']`.

- **`help`** (bool, default: `True`): Whether the parser should automatically print the help message and terminate when `-h` or `--help` option is encountered. Set to `False` to handle help manually.

- **`version`** (any, optional): If supplied, the object will be printed when `--version` is encountered. Could be any printable object, but most likely a string, e.g. `"2.1.0rc1"`.

  > **Note:** When `docopt` is set to automatically handle `-h`, `--help` and `--version` options, you still need to mention them in the usage pattern for this to work.

- **`options_first`** (bool, default: `False`): If set to `True`, all arguments after the first positional argument will be interpreted as positional arguments, even if they look like options. Useful for strict POSIX compatibility or when dispatching to other programs.

### Return Value

Returns a dictionary with options, arguments and commands as keys, spelled exactly like in your help message. Long versions of options are given priority.

**Example:**

```bash
naval_fate.py ship Guardian move 100 150 --speed=15
```

**Returns:**

```python
{
    '--drifting': False,    'mine': False,
    '--help': False,        'move': True,
    '--moored': False,      'new': False,
    '--speed': '15',        'remove': False,
    '--version': False,     'set': False,
    '<name>': ['Guardian'], 'ship': True,
    '<x>': '100',           'shoot': False,
    '<y>': '150'
}
```

## Help Message Format

Help messages consist of 2 parts:

### 1. Usage Pattern

```
Usage: my_program.py [-hso FILE] [--quiet | --verbose] [INPUT ...]
```

**Usage pattern** is a substring of `doc` that starts with `usage:` (case *insensitive*) and ends with a *visibly* empty line.

The first word after `usage:` is interpreted as your program's name. You can specify your program's name several times to signify several exclusive patterns:

```
Usage: my_program.py FILE
       my_program.py COUNT FILE
```

### 2. Option Descriptions

```
-h --help    show this
-s --sorted  sorted output
-o FILE      specify output file [default: ./test.txt]
--quiet      print less text
--verbose    print more text
```

**Option descriptions** consist of a list of options that you put below your usage patterns. It is necessary to list option descriptions to specify:

- synonymous short and long options
- if an option has an argument
- if option's argument has a default value

## Pattern Elements

### Arguments

- **`<arguments>`** or **`ARGUMENTS`**: Positional arguments
  - `my_program.py CONTENT-PATH`
  - `my_program.py <content-path>`

### Options

- **`--options`**: Long and short options
  - `--output`, `-o`
  - Can be stacked: `-oiv` is the same as `-o -i -v`
  - Can have arguments: `--input=FILE`, `-i FILE`, `-iFILE`

### Commands

- **`commands`**: Words that don't follow option or argument conventions
  - Special commands: `"-"` (stdin) and `"--"` (separator)

## Pattern Constructs

- **`[ ]`** (brackets): **Optional** elements
  - `my_program.py [-hvqo FILE]`

- **`( )`** (parens): **Required** elements
  - `my_program.py (--clockwise | --counter-clockwise) TIME`

- **`|`** (pipe): **Mutually exclusive** elements
  - `my_program.py [--left | --right]`

- **`...`** (ellipsis): **One or more** elements
  - `my_program.py FILE ...` (one or more)
  - `my_program.py [FILE ...]` (zero or more)

- **`[options]`**: Shortcut for any options not in usage pattern

## Advanced Features

### Counting Flags

```
Usage: my_program.py [-v | -vv | -vvv]
```

The number of occurrences will be counted. `args['-v']` will be `2` if invoked as `my_program -vv`.

### Collecting Arguments

```
Usage: my_program.py <file> <file> --path=<path>...
```

Invoked with `my_program.py file1 file2 --path=./here --path=./there`:

```python
{
    '<file>': ['file1', 'file2'],
    '--path': ['./here', './there']
}
```

### Default Values

```
--coefficient=K  The K coefficient [default: 2.95]
--output=FILE    Output file [default: test.txt]
```

For repeatable options, defaults are split on whitespace:

```
--repeatable=<arg>  [default: ./here ./there]
# Results in: ['./here', './there']
```

## Examples

We have an extensive list of [examples](https://github.com/docopt/docopt/tree/master/examples) which cover every aspect of functionality:

- **[naval_fate.py](examples/naval_fate.py)** - Classic docopt example
- **[git/](examples/git/)** - Multi-level subcommands (like git)
- **[config_file_example.py](examples/config_file_example.py)** - Integration with config files
- **[validation_example.py](examples/validation_example.py)** - Data validation with schema
- And many more!

## Use Cases

### Subcommands and Multi-Level Help

For git-like applications with subcommands, use the `options_first` parameter:

```python
args = docopt(__doc__, version='2.0', options_first=True)
```

See [examples/git/](https://github.com/docopt/docopt/tree/master/examples/git) for a complete implementation.

### Data Validation

**docopt** does one thing well: it implements your command-line interface. For data validation, use libraries like [schema](https://github.com/halst/schema):

```python
from schema import Schema, And, Or, Use

schema = Schema({
    'FILE': [Use(open, error='FILE should be readable')],
    '--count': Or(None, And(Use(int), lambda n: 0 < n < 5))
})

args = schema.validate(docopt(__doc__))
```

See [validation_example.py](https://github.com/docopt/docopt/tree/master/examples/validation_example.py) for details.

### Configuration Files

Integrate with JSON, YAML, or INI config files:

```python
import json
from docopt import docopt

# Load defaults from config
with open('config.json') as f:
    config = json.load(f)

# Parse command line (overrides config)
args = docopt(__doc__)

# Merge with config taking priority for command line
final_args = {**config, **{k: v for k, v in args.items() if v}}
```

See [config_file_example.py](examples/config_file_example.py) for complete examples.

## Development

We would *love* to hear what you think about **docopt** on our [issues page](http://github.com/docopt/docopt/issues).

Make pull requests, report bugs, suggest ideas and discuss **docopt**.

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest`
5. Submit a pull request

## Porting docopt to Other Languages

We think **docopt** is so good, we want to share it beyond the Python community! All official docopt ports to other languages can be found under the [docopt organization page](http://github.com/docopt) on GitHub.

Available ports:

- **C++**: [docopt.cpp](https://github.com/docopt/docopt.cpp)
- **Go**: [docopt.go](https://github.com/docopt/docopt.go)
- **Rust**: [docopt.rs](https://github.com/docopt/docopt.rs)
- **Ruby**: [docopt.rb](https://github.com/docopt/docopt.rb)
- **PHP**: [docopt.php](https://github.com/docopt/docopt.php)
- **CoffeeScript**: [docopt.coffee](https://github.com/docopt/docopt.coffee)
- And many more!

If your favorite language isn't listed, you can create a port! Use the Python version as a reference implementation. A language-agnostic test suite is bundled with the [Python implementation](http://github.com/docopt/docopt).

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

**docopt** follows [semantic versioning](http://semver.org).

### Quick History

- **1.0.0** (2025-01-04): Python 3.10+ modernization, production stable
- **0.6.2** (2014-06-09): Last Python 2.7 compatible version
- **0.6.0** (2013-02-07): Added `options_first` parameter
- **0.5.0** (2012-10-03): Repeated options/commands support
- **0.1.0** (2012-04-01): Initial release

## License

MIT License. See [LICENSE](LICENSE) for details.

Copyright (c) 2012-2025 Vladimir Keleshev, <vladimir@keleshev.com>

## Links

- **Documentation**: [http://docopt.org](http://docopt.org)
- **Repository**: [https://github.com/docopt/docopt](https://github.com/docopt/docopt)
- **PyPI**: [https://pypi.python.org/pypi/docopt](https://pypi.python.org/pypi/docopt)
- **Issues**: [https://github.com/docopt/docopt/issues](https://github.com/docopt/docopt/issues)

---

*Made with ❤️ by the docopt community*

