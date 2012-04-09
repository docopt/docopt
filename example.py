"""Usage: example.py [options] arguments

Options:
  -h --help            show this help message and exit
  --version            show version and exit
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
  --statistics         count errors and warnings
  --count              print total number of errors and warnings to standard
                       error and set exit code to 1 if total is not null
  --benchmark          measure processing speed
  --testsuite=dir      run regression tests from dir
  --doctest            run doctest on myself

"""
from docopt import docopt


def main(options, arguments):
    print(options)
    print('Arguments: %s' % arguments)


if __name__ == '__main__':
    # parse options based on docstring above
    options, arguments = docopt(__doc__, version='1.0.0rc2')
    main(options, arguments)
