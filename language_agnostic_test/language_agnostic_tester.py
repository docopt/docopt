#! /usr/bin/env python
'''

r"""Usage: prog

"""
$ prog
{}

$ prog --xxx
"user-error"


r"""Usage: prog [options]

-a  All.

"""
$ prog
{"-a": false}

$ prog -a
{"-a": true}

$ prog -x
"user-error"


r"""Usage: prog [options]

--all  All.

"""
$ prog
{"--all": false}

$ prog --all
{"--all": true}

$ prog --xxx
"user-error"


r"""Usage: prog [options]

-v, --verbose  Verbose.

"""
$ prog --verbose
{"--verbose": true}

$ prog --ver
{"--verbose": true}

$ prog -v
{"--verbose": true}


r"""Usage: prog [options]

-p PATH

"""
$ prog -p home/
{"-p": "home/"}

$ prog -phome/
{"-p": "home/"}

$ prog -p
"user-error"


r"""Usage: prog [options]

--path <path>

"""
$ prog --path home/
{"--path": "home/"}

$ prog --path=home/
{"--path": "home/"}

$ prog --pa home/
{"--path": "home/"}

$ prog --pa=home/
{"--path": "home/"}

$ prog --path
"user-error"


r"""Usage: prog [options]

-p PATH, --path=<path>  Path to files.

"""
$ prog -proot
{"--path": "root"}


r"""Usage: prog [options]

   -p --path PATH  Path to files.

"""
$ prog -p root
{"--path": "root"}

$ prog --path root
{"--path": "root"}


r"""Usage: prog [options]

-p PATH  Path to files [default: ./]

"""
$ prog
{"-p": "./"}

$ prog -phome
{"-p": "home"}


r"""UsAgE: prog [options]

--path=<files>  Path to files
                [dEfAuLt: /root]

"""
$ prog
{"--path": "/root"}

$ prog --path=home
{"--path": "home"}


r"""usage: prog [options]

-a        Add
-r        Remote
-m <msg>  Message

"""
$ prog -a -r -m Hello
{"-a": true,
 "-r": true,
 "-m": "Hello"}

$ prog -armyourass
{"-a": true,
 "-r": true,
 "-m": "yourass"}

$ prog -a -r
{"-a": true,
 "-r": true,
 "-m": null}


r"""Usage: prog [options]

--version
--verbose

"""
$ prog --version
{"--version": true,
 "--verbose": false}

$ prog --verbose
{"--version": false,
 "--verbose": true}

$ prog --ver
"user-error"

$ prog --verb
{"--version": false,
 "--verbose": true}


r"""usage: prog [-a -r -m <msg>]

-a        Add
-r        Remote
-m <msg>  Message

"""
$ prog -armyourass
{"-a": true,
 "-r": true,
 "-m": "yourass"}


r"""usage: prog [-armmsg]

-a        Add
-r        Remote
-m <msg>  Message

"""
$ prog -a -r -m Hello
{"-a": true,
 "-r": true,
 "-m": "Hello"}


r"""usage: prog -a -b

-a
-b

"""
$ prog -a -b
{"-a": true, "-b": true}

$ prog -b -a
{"-a": true, "-b": true}

$ prog -a
"user-error"

$ prog
"user-error"


r"""usage: prog (-a -b)

-a
-b

"""
$ prog -a -b
{"-a": true, "-b": true}

$ prog -b -a
{"-a": true, "-b": true}

$ prog -a
"user-error"

$ prog
"user-error"


r"""usage: prog [-a] -b

-a
-b

"""
$ prog -a -b
{"-a": true, "-b": true}

$ prog -b -a
{"-a": true, "-b": true}

$ prog -a
"user-error"

$ prog -b
{"-a": false, "-b": true}

$ prog
"user-error"


r"""usage: prog [(-a -b)]

-a
-b

"""
$ prog -a -b
{"-a": true, "-b": true}

$ prog -b -a
{"-a": true, "-b": true}

$ prog -a
"user-error"

$ prog -b
"user-error"

$ prog
{"-a": false, "-b": false}


r"""usage: prog (-a|-b)

-a
-b

"""
$ prog -a -b
"user-error"

$ prog
"user-error"

$ prog -a
{"-a": true, "-b": false}

$ prog -b
{"-a": false, "-b": true}


r"""usage: prog [ -a | -b ]

-a
-b

"""
$ prog -a -b
"user-error"

$ prog
{"-a": false, "-b": false}

$ prog -a
{"-a": true, "-b": false}

$ prog -b
{"-a": false, "-b": true}


r"""usage: prog <arg>

"""
$ prog 10
{"<arg>": "10"}

$ prog 10 20
"user-error"

$ prog
"user-error"


r"""usage: prog [<arg>]

"""
$ prog 10
{"<arg>": "10"}

$ prog 10 20
"user-error"

$ prog
{"<arg>": null}


r"""usage: prog <kind> <name> <type>

"""
$ prog 10 20 40
{"<kind>": "10", "<name>": "20", "<type>": "40"}

$ prog 10 20
"user-error"

$ prog
"user-error"


r"""usage: prog <kind> [<name> <type>]

"""
$ prog 10 20 40
{"<kind>": "10", "<name>": "20", "<type>": "40"}

$ prog 10 20
{"<kind>": "10", "<name>": "20", "<type>": null}

$ prog
"user-error"


r"""usage: prog [<kind> | <name> <type>]

"""
$ prog 10 20 40
"user-error"

$ prog 20 40
{"<kind>": null, "<name>": "20", "<type>": "40"}

$ prog
{"<kind>": null, "<name>": null, "<type>": null}


r"""usage: prog (<kind> --all | <name>)

--all

"""
$ prog 10 --all
{"<kind>": "10", "--all": true, "<name>": null}

$ prog 10
{"<kind>": null, "--all": false, "<name>": "10"}

$ prog
"user-error"


r"""usage: prog [<name> <name>]

"""
$ prog 10 20
{"<name>": ["10", "20"]}

$ prog 10
{"<name>": ["10"]}

$ prog
{"<name>": []}


r"""usage: prog [(<name> <name>)]

"""
$ prog 10 20
{"<name>": ["10", "20"]}

$ prog 10
"user-error"

$ prog
{"<name>": []}


r"""usage: prog NAME...

"""
$ prog 10 20
{"NAME": ["10", "20"]}

$ prog 10
{"NAME": ["10"]}

$ prog
"user-error"


r"""usage: prog [NAME]...

"""
$ prog 10 20
{"NAME": ["10", "20"]}

$ prog 10
{"NAME": ["10"]}

$ prog
{"NAME": []}


r"""usage: prog [NAME...]

"""
$ prog 10 20
{"NAME": ["10", "20"]}

$ prog 10
{"NAME": ["10"]}

$ prog
{"NAME": []}


r"""usage: prog [NAME [NAME ...]]

"""
$ prog 10 20
{"NAME": ["10", "20"]}

$ prog 10
{"NAME": ["10"]}

$ prog
{"NAME": []}


r"""usage: prog (NAME | --foo NAME)

--foo

"""
$ prog 10
{"NAME": "10", "--foo": false}

$ prog --foo 10
{"NAME": "10", "--foo": true}

$ prog --foo=10
"user-error"


r"""usage: prog (NAME | --foo) [--bar | NAME]

--foo
--bar

"""
$ prog 10
{"NAME": ["10"], "--foo": false, "--bar": false}

$ prog 10 20
{"NAME": ["10", "20"], "--foo": false, "--bar": false}

$ prog --foo --bar
{"NAME": [], "--foo": true, "--bar": true}


r"""Naval Fate.

Usage:
  prog ship new <name>...
  prog ship [<name>] move <x> <y> [--speed=<kn>]
  prog ship shoot <x> <y>
  prog mine (set|remove) <x> <y> [--moored|--drifting]
  prog -h | --help
  prog --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --speed=<kn>  Speed in knots [default: 10].
  --moored      Mored (anchored) mine.
  --drifting    Drifting mine.

"""
$ prog ship Guardian move 150 300 --speed=20
{"--drifting": false,
 "--help": false,
 "--moored": false,
 "--speed": "20",
 "--version": false,
 "<name>": ["Guardian"],
 "<x>": "150",
 "<y>": "300",
 "mine": false,
 "move": true,
 "new": false,
 "remove": false,
 "set": false,
 "ship": true,
 "shoot": false}


r"""usage: prog --hello

"""
$ prog --hello
{"--hello": true}


r"""usage: prog [--hello=<world>]

"""
$ prog
{"--hello": null}

$ prog --hello wrld
{"--hello": "wrld"}


r"""usage: prog [-o]

"""
$ prog
{"-o": false}

$ prog -o
{"-o": true}


r"""usage: prog [-opr]

"""
$ prog -op
{"-o": true, "-p": true, "-r": false}


r"""usage: prog --aabb | --aa

"""
$ prog --aa
{"--aabb": false, "--aa": true}

$ prog --a
"user-error"  # not a unique prefix

#
# test_bug_option_argument_should_not_capture_default_value_from_pattern
#

r"""usage: prog [--file=<f>]

"""
$ prog
{"--file": null}


r"""usage: prog [--file=<f>]

--file <a>

"""
{"--file": null}


r"""Usage: tau [-a <host:port>]

-a, --address <host:port>  TCP address [default: localhost:6283].

"""
$ prog
{"--address": "localhost:6283"}

#
# Counting number of flags
#

r"""Usage: prog -v

"""
$ prog -v
{"-v": true}


r"""Usage: prog [-v -v]

"""
$ prog
{"-v": 0}

$ prog -v
{"-v": 1}

$ prog -vv
{"-v": 2}


r"""Usage: prog -v ...

"""
$ prog
"user-error"

$ prog -v
{"-v": 1}

$ prog -vv
{"-v": 2}

$ prog -vvvvvv
{"-v": 6}


r"""Usage: prog [-v | -vv | -vvv]

This one is probably most readable user-friednly variant.

"""
$ prog
{"-v": 0}

$ prog -v
{"-v": 1}

$ prog -vv
{"-v": 2}

$ prog -vvvv
"user-error"


r"""usage: prog [--ver --ver]

"""
$ prog --ver --ver
{"--ver": 2}


#
# Counting commands
#

r"""usage: prog [go]

"""
$ prog go
{"go": true}


r"""usage: prog [go go]

"""
$ prog
{"go": 0}

$ prog go
{"go": 1}

$ prog go go
{"go": 2}

$ prog go go go
"user-error"

r"""usage: prog go...

"""
$ prog go go go go go
{"go": 5}


#
# test_accumulate_multiple_options
#

r"""usage: prog --long=<arg> ...

"""
$ prog --long one
{"--long": ["one"]}

$ prog --long one --long two
{"--long": ["one", "two"]}


#
# test_multiple_different_elements
#

r"""usage: prog (go <direction> --speed=<km/h>)...

"""
$ prog go left --speed=5  go right --speed=9
{"go": 2, "<direction>": ["left", "right"], "--speed": ["5", "9"]}

'''
import sys, json, re
from subprocess import Popen, PIPE, STDOUT

# remove comments
__doc__ = re.sub('#.*$', '', __doc__, flags=re.M)

testee = (sys.argv[1] if len(sys.argv) >= 2 else
        exit('Usage: language_agnostic_tester.py ./path/to/executable/testee [ID ...]'))
ids = [int(x) for x in sys.argv[2:]] if len(sys.argv) > 2 else None
summary = ''

index = 0
for fixture in __doc__.split('r"""'):
    doc, _, body = fixture.partition('"""')
    for case in body.split('$')[1:]:
        index += 1
        if ids is not None and index not in ids:
            continue
        argv, _, expect = case.strip().partition('\n')
        prog, _, argv = argv.strip().partition(' ')
        assert prog == 'prog', repr(prog)
        p = Popen(testee + ' ' + argv,
                  stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)
        result = p.communicate(input=doc)[0]
        try:
            py_result = json.loads(result)
            py_expect = json.loads(expect)
        except:
            summary += 'J'
            print (' %d: BAD JSON ' % index).center(79, '=')
            print 'result>', result
            print 'expect>', expect
            continue
        if py_result == py_expect:
            summary += '.'
        else:
            print (' %d: FAILED ' % index).center(79, '=')
            print 'r"""%s"""' % doc
            print '$ prog %s\n' % argv
            print 'result>', result
            print 'expect>', expect
            summary += 'F'

print (' %d / %d ' % (summary.count('.'), len(summary))).center(79, '=')
print summary
