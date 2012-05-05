.. docopt documentation master file, created by
   sphinx-quickstart on Mon Apr 23 17:33:34 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
   Welcome to docopt's documentation!
   ==================================
   Contents:
   .. toctree::
   :maxdepth: 2
   Indices and tables
   ==================
   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`


``docopt``---pythonic option parser, that will make you smile
===============================================================================

::

    pip install docopt

Isn't it awesome how ``optparse`` and ``argparse`` generate help and
usage-messages based on your code?!

Hell no!  You know what's awesome?  It's when the option parser *is* generated
based on the help and usage-message that you write in a docstring!  This way
you don't need to write this stupid repeatable parser-code, and instead can
write a beautiful usage-message (the way you want it!), which adds readability
to your code.

Imagine you are writing a program and thinking to allow it's usage as follows::

    Usage: prog [-vqrh] [FILE]
           prog (--left | --right) CORRECTION FILE

Using argparse you will end writing something like this::

    import argparse
    import sys


    def process_arguments():
        parser = argparse.ArgumentParser(
                description='Process FILE and optionally apply correction to '
                            'either left-hand side or right-hand side.')
        parser.add_argument('correction', metavar='CORRECTION', nargs='?',
                            help='correction angle, needs FILE, --left or '
                                 '--right to be present')
        parser.add_argument('file', metavar='FILE', nargs='?',
                            help='optional input file')
        parser.add_argument('-v', dest='v', action='store_true',
                            help='verbose mode')
        parser.add_argument('-q', dest='q', action='store_true',
                            help='quiet mode')
        parser.add_argument('-r', dest='r', action='store_true',
                            help='make report')
        left_or_right = parser.add_mutually_exclusive_group(required=False)
        left_or_right.add_argument('--left', dest='left', action='store_true',
                            help='use left-hand side')
        left_or_right.add_argument('--right', dest='right', action='store_true',
                            help='use right-hand side')
        arguments = parser.parse_args()
        if (arguments.correction and not (arguments.left or arguments.right)
                and not arguments.file):
            sys.stderr.write('correction angle, needs FILE, --left or --right '
                             'to be present')
            parser.print_help()
        return arguments


    def main(arguments):
        # ...


    if __name__ == '__main__':
        main(process_arguments())

While ``docopt`` allows you to write an awesome, readable, clean, pythonic code
like *that*::

    """Usage: prog [-vqrh] [FILE]
              prog (--left | --right) CORRECTION FILE

    Process FILE and optionally apply correction to either left-hand side or
    right-hand side.

    Arguments:
      FILE        optional input file
      CORRECTION  correction angle, needs FILE, --left or --right to be present

    Options:
      -h --help
      -v       verbose mode
      -q       quiet mode
      -r       make report
      --left   use left-hand side
      --right  use right-hand side

    """
    from docopt import docopt


    def main(options, arguments):
        # ...


    if __name__ == '__main__':
        # parse arguments based on docstring above
        options, arguments = docopt(__doc__)
        main(options, arguments)

Yep! The option parser is generated based on docstring above, that you
pass to the ``docopt`` function.  ``docopt`` parses the usage-message and
ensures that program invocation matches it; it parses both options and
arguments based on that. The basic idea is that *a good usage-message
has all necessary information in it to make a parser*.

Also, the practice of putting usage-message in module's docstring
is endorsed by `pep257 <http://www.python.org/dev/peps/pep-0257/>`_:

    The docstring of a script (a stand-alone program) should be usable as its
    "usage" message, printed when the script is invoked with incorrect or
    missing arguments (or perhaps with a "-h" option, for "help"). Such a
    docstring should document the script's function and command line syntax,
    environment variables, and files. Usage messages can be fairly elaborate
    (several screens full) and should be sufficient for a new user to use the
    command properly, as well as a complete quick reference to all options and
    arguments for the sophisticated user.

By the way, ``docopt`` is tested with Python 2.6, 2.7 and 3.2.

API
===============================================================================

::

    from docopt import docopt

.. function:: docopt(doc[, args=sys.argv[1:]][, help=True][, version=None])

``docopt`` takes 1 required and 3 optional arguments:

- ``doc`` should be a module docstring (``__doc__``) or some other string that
  describes **usage-message** in a human-readable format, that will be
  parsed to create the option parser.  The simple rules of how to write such a
  docstring (in order to generate option parser from it successfully) are given
  in the next section. Here is a quick example of such a string::

    """Usage: your_program.py [-hvo FILE] [--quiet] INPUT

    -h --help     show this
    -v --verbose  print more text
    --quiet       print less text
    -o FILE       specify output file [default: ./test.txt]

    """

- ``args`` is an optional argument; by default it is supplied with options and
  arguments passed to your program (``sys.argv[1:]``). In case you want to
  supply something else, it should be in the format similar to ``sys.argv``,
  i.e. a list of strings, such as ``['--verbose', '-o', 'hai.txt']``.

- ``help``, by default ``True``, specifies whether the parser should
  automatically print the usage-message (supplied as ``doc``) and terminate,
  in case ``-h`` or ``--help`` options are encountered. If you want to handle
  ``-h`` or ``--help`` options manually (as all other options), set
  ``help=False``.

- ``version``, by default ``None``, is an optional argument that specifies the
  version of your program. If supplied, then, if the parser encounters
  ``--version`` option, it will print the supplied version and terminate.
  ``version`` could be any printable object, but most likely a string,
  e.g. ``"2.1.0rc1"``.

.. note:: when ``docopt`` is set to automatically handle ``-h``, ``--help`` and
   ``--version`` options, you still need to mention them in the options
   description (``doc``) for your users to know about them.

The **return** value is a tuple ``options, arguments``, where:

- ``options`` is a namespace with options values.
  It can be pretty-printed for debugging (try ``example.py``). Names of
  instance variables will be based on option names, so that characters
  that are not allowed in an instance variable name (such as dash ``-``) will
  be substituted with underscore ``_``. E.g. option ``--print-out`` will be
  presented as ``options.print_out``, and option ``-v, --verbose`` will be
  presented as ``options.verbose``, giving precedence to a longer variant.

- ``arguments`` is a namespace with arguments values.

Docstring format for your usage-message
===============================================================================

The main idea behind ``docopt`` is that a good usage-message (that describes
options and defaults unambiguously) is enough to generate an option parser.

Here are the simple rules (that you probably already follow) for your
usage-message to be parsable:

- Every line that starts with ``-`` or ``--`` (not counting spaces) is treated
  as an option description, e.g.::

    """
    Options:
      --verbose   # GOOD
      -o FILE     # GOOD
    Other: --bad  # BAD, line does not start with dash "-"
    """

- To specify that an option has an argument, put a word describing that
  argument after space (or equals ``=`` sign) as shown below.
  You can use comma if you want to separate options. In the example below both
  lines are valid, however you are recommended to stick to a single style. ::

    """
    -o FILE --output=FILE       # without comma, with "=" sign
    -i <file>, --input <file>   # with comma, wihtout "=" sing
    """

- Use two spaces to separate options with their informal description. ::

    """
    --verbose More text.   # BAD, will be treated as if verbose option had
                           # an argument "More", so use 2 spaces instead
    -q        Quit.        # GOOD
    -o FILE   Output file. # GOOD
    --stdout  Use stdout.  # GOOD, 2 spaces
    """

- If you want to set a default value for an option with an argument, put it
  into the option description, in form ``[default: <your-default-value>]``.
  To be precise, it should match the following regular expression:
  ``"\[default: (.*)\]"``.
  The parser will try to interprete the default value as Python literal
  (using ``ast.literal_eval``), and if it can't, it will be interpreted as a
  string, e.g.::

    """
    -i INSTANCE      Instance of something [default: 1]  # will be int
    --coefficient=K  The K coefficient [default: 2.95]   # will be float
    --output=FILE    Output file [default: "test.txt"]   # will be str
    --directory=DIR  Some directory [default: ./]        # will be str "./"
    """

Note, that ``docopt`` also tries to interprete passed arguments of options as
Python literals, or else as strings, so in most cases you don't need to
convert types.

Something missing?
===============================================================================

Missing a feature from your current option-parser? Together we can make
``docopt`` better, so send a patch or pull-request.
