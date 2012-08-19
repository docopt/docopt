"""Usage: prog.py --count=N OUTDIR FILE

Arguments:
  FILE     input file
  OUTDIR   out directory

Options:
  --count NUM   number of operations [default: 1]

"""
import docopt
try:
    import voluptuous as v
except ImportError:
    exit('This example assumes that `voluptuous` data-validation library\n'
         'is installed: pip install voluptuous\n'
         'https://github.com/alecthomas/voluptuous')

if __name__ == '__main__':
    args = docopt.docopt(__doc__)

    schema = v.Schema({
        'FILE': v.isfile('FILE does not exist.'),
        'OUTDIR': v.isdir('OUTDIR directory does not exist.'),
        '--count': v.all(v.coerce(int, '--count should be integer.'),
                         v.clamp(min=1, max=5))})
    try:
        args = schema(args)
    except v.Invalid as ex:
        exit('\n'.join(['error: ' + e.msg.split('.')[0] for e in ex.errors]))

    print(args)
