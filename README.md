
`docopt` – pythonic option parser, that will make you smile
===============================================================================

Isn't it awesome how `optparse` and `argparse` generate help and usage-messages
based on your code?!

Hell no!  You know what's awesome?  It's when the option parser *is* generated
based on the help and usage-message that you write in a docstring!  This way
you don't need to write this stupid repeatable parser-code, and instead can
write a beautiful usage-message (the way you want it!), which adds readability
to your code.

So instead of writing shit like this (typical example):

```python
from optparse import OptionParser


def process_options():
    parser = OptionParser(usage="program.py [options] arguments")
    parser.add_option('-v', '--verbose', action='store_true',
                      help="print status messages")
    parser.add_option('-q', '--quiet', action='store_true',
                      help="report only file names")
    parser.add_option('-r', '--repeat', action='store_true',
                      help="show all occurrences of the same error")
    parser.add_option('--exclude', metavar='patterns',
                      default='.svn,CVS,.bzr,.hg,.git',
                      help="exclude files or directories which match these "
                        "comma separated patterns [default: %s]" %
                        '.svn,CVS,.bzr,.hg,.git')
    parser.add_option('--filename', metavar='patterns', default='*.py',
                      help="when parsing directories, only check filenames "
                        "matching these comma separated patterns "
                        "[default: *.py]")
    parser.add_option('--select', metavar='errors',
                      help="select errors and warnings (e.g. E,W6)")
    parser.add_option('--ignore', metavar='errors',
                      help="skip errors and warnings (e.g. E4,W)")
    parser.add_option('--show-source', action='store_true',
                      help="show source code for each error")
    options, arguments = parser.parse_args()
    return options, arguments


def main(options, arguments):
    pass  # ...


if __name__ == '__main__':
    options, arguments = process_options()
    main(options, arguments)
```

You can write an awesome, readable, clean, pythonic code like *that*:

```python
"""Usage: program.py [options] arguments

Options:
  -h --help            show this help message and exit
  -v --verbose         print status messages
  -q --quiet           report only file names
  -r --repeat          show all occurrences of the same error
  --exclude=patterns   exclude files or directories which match these comma
                       separated patterns [default: .svn,CVS,.bzr,.hg,.git]
  --filename=patterns  when parsing directories, only check filenames matching
                       these comma separated patterns [default: *.py]
  --select=errors      select errors and warnings (e.g. E,W6)
  --ignore=errors      skip errors and warnings (e.g. E4,W)
  --show-source        show source code for each error

"""
from docopt import docopt


def main(options, arguments):
    pass  # ...


if __name__ == '__main__':
    # parse options based on docstring above
    options, arguments = docopt(__doc__)
    main(options, arguments)
```

Fuck yeah! The option parser is generated based on docstring above, that you
pass to the `docopt` funciton.

Also, the practice of putting usage-message in module's docstring
is endorsed by [pep257](http://www.python.org/dev/peps/pep-0257/):

> The docstring of a script (a stand-alone program) should be usable as its
> "usage" message, printed when the script is invoked with incorrect or
> missing arguments (or perhaps with a "-h" option, for "help"). Such a
> docstring should document the script's function and command line syntax,
> environment variables, and files. Usage messages can be fairly elaborate
> (several screens full) and should be sufficient for a new user to use the
> command properly, as well as a complete quick reference to all options and
> arguments for the sophisticated user.

By the way, `docopt` is tested with Python 2.6, 2.7 and 3.2.

API `from docopt import docopt`
===============================================================================

###`options, arguments = docopt(doc[, args=sys.argv[1:], help=True, version=None])`

`docopt` takes 1 required and 3 optional arguments:

- `doc` should be a module docstring (`__doc__`) or some other string that
describes **options** in a human-readable format, that will be parsed to create
the option parser.  The simple rules of how to write such a docstring
(in order to generate option parser from it successfully) are given in the next
section. Here is a quick example of such a string:

        """Usage: your_program.py [options]

        -h --help     Show this.
        -v --verbose  Print more text.
        --quiet       Print less text.
        -o FILE       Specify output file [default: ./test.txt]."""

- `args` is an optional argument; by default it is supplied with options and
arguments passed to your program (`sys.argv[1:]`). In case you want to supply
something else, it should be in the format similar to `sys.argv`, i.e. a list
of strings, such as `['--verbose', '-o', 'hai.txt']`.

- `help`, by default `True`, specifies whether the parser should automatically
print the usage-message (supplied as `doc`) in case `-h` or `--help` options
are encountered. After showing the usage-message, the program will terminate.
If you want to handle `-h` or `--help` options manually (as all other options),
set `help=False`.

- `version`, by default `None`, is an optional argument that specifies the
version of your program. If supplied, then, if the parser encounters
`--version` option, it will print the supplied version and terminate.
`version` could be any printable object, but most likely a string,
e.g. `"2.1.0rc1"`.

Note, when `docopt` is set to automatically handle `-h`, `--help` and
`--version` options, you still need to mention them in the options description
(`doc`) for your users to know about them.

The **return** value is a tuple `options, arguments`, where:

- `options` is an object with instance variables corresponding to each option.
It can be pretty-printed for debugging (try `example.py`). Names of
instance variables will be based on option names, so that characters
that are not allowed in an instance variable name (such as dash `-`) will be
substituted with underscore `_`. E.g. option `--print-out` will be
presented as `options.print_out`, and option `-v, --verbose` will be
presented as `options.verbose`, giving precedence to a longer variant.

- `arguments` is a list of non-option arguments.

Docstring format for your usage-message
===============================================================================

The main idea behind `docopt` is that a good usage-message (that describes
options and defaults unambiguously) is enough to generate an option parser.

Here are the simple rules (that you probably already follow) for your
usage-message to be parsable:

- Every line that starts with `-` or `--` (not counting spaces) is treated
as an option description, e.g.:

        """
        Options:
          --verbose   # GOOD
          -o FILE     # GOOD
        Other: --bad  # BAD, line does not start with dash "-"
        """

- To specify that an option has an argument, put a word describing that
argument after space (or equals `=` sign) as shown below.
You can use comma if you want to separate options. In the example below both
lines are valid, however you are recommended to stick to a single style.

        """
        -o FILE --output=FILE       # without comma, with "=" sign
        -i <file>, --input <file>   # with comma, wihtout "=" sing
        """

- Use two sapaces to separate options with their informal description.

        """
        --verbose More text.   # BAD, will be treated as if verbose option had
                               # an argument "More", so use 2 spaces instead
        -q        Quit.        # GOOD
        -o FILE   Output file. # GOOD
        --stdout  Use stdout.  # GOOD, 2 spaces
        """

- If you want to set a default value for an option with an argument, put it
into the option description, in form `[default: <your-default-value>]`.
To be precise, it should match the following regular expression:
`"\[default: (.*)\]"`.
The parser will try to interprete the default value as Python literal
(using `ast.literal_eval`), and if it can't, it will be interpreted as a
string, e.g.:

        """
        -i INSTANCE      Instance of something [default: 1]  # will be int
        --coefficient=K  The K coefficient [default: 2.95]   # will be float
        --output=FILE    Output file [default: "test.txt"]   # will be str
        --directory=DIR  Some directory [default: ./]        # will be str "./"
        """

Note, that `docopt` also tries to interprete passed arguments of options as
Python literals, or else as strings, so in most cases you don't need to
convert types.

Something missing?
===============================================================================

Missing a feature from your current option-parser? Together we can make
`docopt` better, so send a patch or pull-request.
