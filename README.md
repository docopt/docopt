
`docopt` - pythonic option parser, that will make you happy!
-------------------------------------------------------------------------------

Isn't it awesome how `optparse` and `argparse` generate help and usage messages
based on your code?!  

Hell no!  You know what's awesome?  It's when the option parser *is* generated
based on the help and usage message that you write in a docstring!

So instead of writing shit like this:

    from optparse import OptionParser


    def process_options():
        parser = OptionParser(usage="%prog [options] input ...")
        parser.add_option('-v', '--verbose', action='store_true',
                          help="print status messages")
        parser.add_option('-q', '--quiet', action='store_true',
                          help="report only file names")
        parser.add_option('-r', '--repeat', action='store_true',
                          help="show all occurrences of the same error")
        parser.add_option('--exclude', metavar='patterns',
                          default='.svn,CVS,.bzr,.hg,.git',
                          help="exclude files or directories which match these "
                            "comma separated patterns (default: %s)" %
                            '.svn,CVS,.bzr,.hg,.git')
        parser.add_option('--filename', metavar='patterns', default='*.py',
                          help="when parsing directories, only check filenames "
                            "matching these comma separated patterns (default: "
                            "*.py)")
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


You write an awesome, readable, clean, pythonic code like *that*:

  
    """Usage: pep8.py [options] input ...

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


Fuck yeah!
