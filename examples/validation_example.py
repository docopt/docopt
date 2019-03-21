"""Usage: prog.py [--count=N] PATH FILE...

Arguments:
  FILE     input file
  PATH     out directory

Options:
  --count=N   number of operations

"""
import os

from docopt import docopt

try:
    from schema import Schema, And, Or, Use, SchemaError
except ImportError:
    exit("This example requires that `schema` data-validation library" " is installed: \n    pip install schema\n" "https://github.com/halst/schema")


if __name__ == "__main__":
    args = docopt(__doc__)

    schema = Schema(
        {
            "FILE": [Use(open, error="FILE should be readable")],
            "PATH": And(os.path.exists, error="PATH should exist"),
            "--count": Or(None, And(Use(int), lambda n: 0 < n < 5), error="--count=N should be integer 0 < N < 5"),
        }
    )
    try:
        args = schema.validate(args)
    except SchemaError as e:
        exit(e)

    print(args)
