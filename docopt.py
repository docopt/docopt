import re
import sys
from ast import literal_eval
from getopt import gnu_getopt as getopt


class Option(object):

    def __init__(self, short=None, long=None, value=False, parse=None):
        if parse:
            split = parse.strip().split('  ')
            options = split[0].replace(',', ' ').replace('=', ' ')
            description = ''.join(split[1:])
            matched = re.findall('\[default: (.*)\]', description)
            if matched:
                try:
                    value = literal_eval(matched[0])
                except (ValueError, SyntaxError):
                    value = matched[0]
            has_argument = False
            for s in options.split():
                if s.startswith('--'):
                    long = s.lstrip('-')
                elif s.startswith('-'):
                    short = s.lstrip('-')
                else:
                    has_argument = True
            if has_argument:
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

    @property
    def is_flag(self):
        if self.short:
            return not self.short.endswith(':')
        if self.long:
            return not self.long.endswith('=')

    def __repr__(self):
        return 'Option(%s, %s, %s)' % (repr(self.short),
                                       repr(self.long),
                                       repr(self.value))

    def __eq__(self, other):
        return repr(self) == repr(other)


class Options(object):

    def __init__(self, **kw):
        self.__dict__ = kw

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __repr__(self):
        return 'Options(%s)' % ', '.join(["%s=%s" % (kw, repr(a))
                                        for kw, a in self.__dict__.items()])


def parse_doc(doc):
    return [Option(parse='-' + s) for s in re.split('\n *-', doc)[1:]]


def docopt(doc, args=sys.argv[1:]):
    docopts = parse_doc(doc)
    getopts, args = getopt(args,
                           ''.join([d.short for d in docopts if d.short]),
                           [d.long for d in docopts if d.long])
    for k, v in getopts:
        for o in docopts:
            if k in o.forms:
                o.value = True if o.is_flag else v
    return Options(**dict([(o.name, o.value) for o in docopts])), args


