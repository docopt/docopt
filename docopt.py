from getopt import gnu_getopt, GetoptError
from ast import literal_eval
import sys
import re


class Option(object):

    def __init__(self, short=None, long=None, value=False, parse=None):
        self.is_flag = True
        if parse:
            split = parse.strip().split('  ')
            options = split[0].replace(',', ' ').replace('=', ' ')
            description = ''.join(split[1:])
            for s in options.split():
                if s.startswith('--'):
                    long = s.lstrip('-')
                elif s.startswith('-'):
                    short = s.lstrip('-')
                else:
                    self.is_flag = False
            if not self.is_flag:
                matched = re.findall('\[default: (.*)\]', description)
                value = argument_eval(matched[0]) if matched else False
                short = short + ':' if short else None
                long = long + '=' if long else None
        self.short = short
        self.long = long
        self.value = value

    @property
    def name(self):
        s = self.long or self.short
        s = s.rstrip(':').rstrip('=')
        ret = s[0] if s[0].isalpha() else '_'
        for ch in s[1:]:
            ret += ch if ch.isalpha() or ch.isdigit() else '_'
        return ret

    @property
    def forms(self):
        if self.short:
            yield '-' + self.short.rstrip(':')
        if self.long:
            yield '--' + self.long.rstrip('=')

    def __repr__(self):
        return 'Option(%s, %s, %s)' % (repr(self.short),
                                       repr(self.long),
                                       repr(self.value))

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __ne__(self, other):
        return not self == other


class Options(object):

    def __init__(self, **kw):
        self.__dict__ = kw

    def __eq__(self, other):
        return type(self) is type(other) and \
            self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return 'Options(%s)' % ',\n    '.join("%s=%s" % (kw, repr(a))
                                           for kw, a in self.__dict__.items())


def argument_eval(s):
    try:
        return literal_eval(s)
    except (ValueError, SyntaxError):
        return s


def docopt(doc, args=sys.argv[1:], help=True, version=None):
    docopts = [Option(parse='-' + s) for s in re.split('^ *-|\n *-', doc)[1:]]
    try:
        getopts, args = gnu_getopt(args,
                            ''.join(d.short for d in docopts if d.short),
                            [d.long for d in docopts if d.long])
    except GetoptError as e:
        exit(e.msg)
    for k, v in getopts:
        for o in docopts:
            if k in o.forms:
                o.value = True if o.is_flag else argument_eval(v)
            if help and k in ('-h', '--help'):
                exit(doc.strip())
            if version is not None and k == '--version':
                exit(version)
    return Options(**dict((o.name, o.value) for o in docopts)), args
