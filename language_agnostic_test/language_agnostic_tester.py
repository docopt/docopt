#! /usr/bin/env python
import sys, json, re, os
from subprocess import Popen, PIPE, STDOUT

fixtures = open(os.path.join(os.path.dirname(__file__), 'testcases.docopt'), 'r').read()

# remove comments
fixtures = re.sub('#.*$', '', fixtures, flags=re.M)

testee = (sys.argv[1] if len(sys.argv) >= 2 else
        exit('Usage: language_agnostic_tester.py ./path/to/executable/testee [ID ...]'))
ids = [int(x) for x in sys.argv[2:]] if len(sys.argv) > 2 else None
summary = ''

index = 0
for fixture in fixtures.split('r"""'):
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
