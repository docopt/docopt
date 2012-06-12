#! /usr/bin/env python
from docopt import docopt, DocoptExit
import sys, json

doc = sys.stdin.read()

try:
    print json.dumps(docopt(doc))
except DocoptExit:
    print '"user-error"'
