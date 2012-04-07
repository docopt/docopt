"""Usage: %prog [options] [--dummy | SERIAL_PORT]

Message Center client for ABB Modbus device

--version   show program's version number and exit
-h, --help  show this help message and exit
--dump      print values instead of sending them to Message Center
--dummy     use dummy Modbus for testing
--message-center=HOST:PORT
            message center HOST:PORT [default: 127.0.0.1:1042]
--sampling-period=SECONDS
            data sampling period in seconds [default: 3]
--offset=+1/0/-1
            address offset [default: 0]
--holding   read holding registers, instead of input registers

"""
def parse_options():
    options, arguments = docopt(__doc__, version=__version__)

def parse_options():
    parser = OptionParser(version=__version__,
          usage="%prog [options] [--dummy | SERIAL_PORT]",
          description='Message Center client for ABB Modbus device')
    parser.add_option('--dump', action='store_true',
        help='print values instead of sending them to Message Center')
    parser.add_option('--dummy', action='store_true',
        help='use dummy Modbus for testing')
    parser.add_option('--message-center', action="store", type="string",
        default='127.0.0.1:1042', metavar='HOST:PORT',
        help='message center HOST:PORT, by default: 127.0.0.1:1042')
    parser.add_option('--sampling-period', action="store", type="float",
                      default=3.0, metavar='SECONDS',
                      help='data sampling period, by default: 3 seconds')
    parser.add_option('--offset', action="store", type="int",
                      default=0, metavar='+1/0/-1',
                      help='address offset, by default: 0')
    parser.add_option('--holding', action='store_true',
        help='read holding registers, instead of input registers')
    return parser.parse_args()
