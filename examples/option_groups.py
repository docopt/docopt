"""Example of program with many options groups using docopt.

Usage:
  option_groups.py [--port=<port>] [cert_opts] [options] serve <fsroot>
  option_groups.py [--port=<port>] [cert_opts] [options] upload <host> <file>...
  option_groups.py [options] changes <local_dir>
  option_groups.py (-h | --help)
  option_groups.py --version

Arguments:
  <fsroot>                  local directory to serve
  <file>                    file(s) to upload
  <local_dir>               directory to check for local changes

Certificate options [cert_opts]:
  --certfile=<certfile>     X509 certificate
  --keyfile=<keyfile>       key for certificate

General options [options]:
  -v --verbose              print status messages

Other options:
  -h --help                 show this help message and exit
  --version                 show version and exit
  -p <port> --port=<port>   port to use

"""
from docopt import docopt


if __name__ == '__main__':
    arguments = docopt(__doc__, version='1.0.0')
    print(arguments)
