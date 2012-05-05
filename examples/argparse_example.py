import argparse
import sys


def process_arguments():
    parser = argparse.ArgumentParser(
            description='Process FILE and optionally apply correction to '
                        'either left-hand side or right-hand side.')
    parser.add_argument('correction', metavar='CORRECTION', nargs='?',
                        help='correction angle, needs FILE, --left or --right '
                             'to be present')
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
    print(arguments)


if __name__ == '__main__':
    main(process_arguments())
