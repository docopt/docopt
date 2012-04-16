from ast import literal_eval
from copy import deepcopy
import sys
import re


class DocoptError(Exception):
    pass


class Pattern(object):

    def __init__(self, *args):
        self.args = args

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__,
                           ', '.join([repr(a) for a in self.args]))


class Argument(Pattern):

    def __init__(self, meta):
        self.meta = meta
        self.args = [meta]

    @property
    def name(self):
        return self.args[0].strip('<>').lower()

    def match(self, left):
        args = [l for l in left if type(l) == Argument]
        if not len(args):
            return False, left
        left.remove(args[0])
        return True, left


class Option(Pattern):

    def __init__(self, short=None, long=None, value=False, parse=None):
        self.short = short
        self.long = long
        self.value = value

    def match(self, left):
        left_ = []
        for l in left:
            if not (type(l) == Option and
                    (self.short, self.long) == (l.short, l.long)):
                left_.append(l)
        return (left != left_), left_

    @property
    def is_flag(self):
        if self.short:
            return not self.short.endswith(':')
        if self.long:
            return not self.long.endswith('=')

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
        return 'Option(%r, %r, %r)' % (self.short, self.long, self.value)


class VerticalBar(object):
    pass


class Parens(Pattern):

    def match(self, left):
        left = deepcopy(left)
        matched = True
        for p in self.args:
            m, left = p.match(left)
            if not m:
                matched = False
        return matched, left


class Brackets(Pattern):

    def match(self, left):
        left = deepcopy(left)
        for p in self.args:
            m, left = p.match(left)
        return True, left


class OneOrMore(Pattern):

    def match(self, left):
        left_ = deepcopy(left)
        matched = True
        while matched:
            matched, left_ = self.args[0].match(left_)
        return (left != left_), left_


class Namespace(object):

    def __init__(self, **kw):
        self.__dict__ = kw

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __ne__(self, other):
        return repr(self) != repr(other)

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__,
                ',\n    '.join(["%s=%s" % (kw, repr(a))
                                for kw, a in self.__dict__.items()]))


class Options(Namespace):
    pass


class Arguments(Namespace):
    pass


def option(parse):
    is_flag = True
    short, long, value = None, None, False
    split = parse.strip().split('  ')
    options = split[0].replace(',', ' ').replace('=', ' ')
    description = ''.join(split[1:])
    for s in options.split():
        if s.startswith('--'):
            long = s.lstrip('-')
        elif s.startswith('-'):
            short = s.lstrip('-')
        else:
            is_flag = False
    if not is_flag:
        matched = re.findall('\[default: (.*)\]', description)
        value = argument_eval(matched[0]) if matched else False
        short = short + ':' if short else None
        long = long + '=' if long else None
    return Option(short, long, value)


def argument_eval(s):
    try:
        return literal_eval(s)
    except (ValueError, SyntaxError):
        return s


def do_longs(parsed, raw, options, parse):
    try:
        i = raw.index('=')
        raw, value = raw[:i], raw[i + 1:]
    except ValueError:
        value = None
    opt = [o for o in options if o.long and o.long.startswith(raw)]
    if len(opt) < 1:
        raise DocoptError('--%s is not recognized' % raw)
    if len(opt) > 1:
        raise DocoptError('--%s is not a unique prefix: %s?' % (raw,
                ', '.join('--%s' % o.long for o in opt)))
    opt = opt[0]
    if not opt.is_flag:
        if value is None:
            if not parse:
                raise DocoptError('--%s requires argument' % opt)
            value, parse = parse[0], parse[1:]
    elif value is not None:
        raise DocoptError('--%s must not have an argument' % opt)
    opt.value = value or True
    parsed += [opt]
    return parsed, parse


def do_shorts(parsed, raw, options, parse):
    while raw != '':
        opt = [o for o in options if o.short and o.short.startswith(raw[0])]
        assert len(opt) == 1
        opt = opt[0]
        raw = raw[1:]
        if opt.is_flag:
            value = True
        else:
            if raw == '':
                if not parse:
                    raise DocoptError('opt -%s requires argument' % opt)
                raw, parse = parse[0], parse[1:]
            value, raw = raw, ''
        opt.value = value
        parsed += [opt]
    return parsed, parse


def pattern(source, options=None):
    return parse(source=source, options=options, is_pattern=True)


def parse(source, options=None, is_pattern=False):
    options = [] if options is None else deepcopy(options)
    if type(source) == str and is_pattern:
        # add space around tokens []()|... for easier parsing
        source = re.sub(r'([\[\]\(\)\|]|\.\.\.)', r' \1 ', source)
    source = source.split() if type(source) == str else source
    parsed = []
    while source:
        if is_pattern and source[0] == '...':
            parsed[-1] = OneOrMore(parsed[-1])
            source = source[1:]
        elif is_pattern and source[0] == '|':
            parsed += [VerticalBar]
            source = source[1:]
        elif is_pattern and source[0] == '[':
            matching = [i for i, e in enumerate(source)
                        if e == ']'][source.count('[') - 1]
            sub_parse = source[1:matching]
            parsed += [Brackets(*parse(sub_parse, is_pattern=is_pattern,
                                       options=options))]
            source = source[matching + 1:]
        elif is_pattern and source[0] == '(':
            matching = [i for i, e in enumerate(source)
                        if e == ')'][source.count('(') - 1]
            sub_parse = source[1:matching]
            parsed += [Parens(*parse(sub_parse, is_pattern=is_pattern,
                                     options=options))]
            source = source[matching + 1:]
        elif source[0] == '--':
            parsed += [Argument(v) for v in parsed[1:]]
            break
        elif source[0][:2] == '--':
            parsed, source = do_longs(parsed, source[0][2:],
                                      options, source[1:])
        elif source[0][:1] == '-' and source[0] != '-':
            parsed, source = do_shorts(parsed, source[0][1:],
                                       options, source[1:])
        else:
            parsed += [Argument(source[0])]
            source = source[1:]
    return parsed


def parse_doc_options(doc):
    return [option('-' + s) for s in re.split('^ *-|\n *-', doc)[1:]]


def parse_doc_usage(doc, options=[]):
    raw_usage = re.split(r'\n\s*\n', re.split(r'[Uu]sage:', doc)[1])[0].strip()
    prog = raw_usage.split()[0]
    raw_patterns = raw_usage.strip(prog).split(prog)
    return [p.strip() for p in raw_patterns]
    #return [Parens(*pattern(s, options=options)) for s in raw_patterns]


def docopt(doc, args=sys.argv[1:], help=True, version=None):
    options = parse_doc_options(doc)
    raw_patterns = parse_doc_usage(doc)
    arg_metavars = [parse(p, options=options) for p in raw_patterns]
    meta = [a.meta for a in sum(arg_metavars, []) if type(a) == Argument]
    try:
        args = parse(args, options=options)
    except DocoptError as e:
        exit(e.message)
    options += [o for o in args if type(o) is Option]
    if help and any(o for o in options
            if (o.short == 'h' or o.long == 'help') and o.value):
        exit(doc.strip())
    if version and any(o for o in options if o.long == 'version' and o.value):
        exit(str(version))
    arguments = [a for a in args if type(a) is Argument]
    return (Options(**dict([(o.name, o.value) for o in options])),
            Arguments(**dict([(m, a.meta) for m, a in zip(meta, arguments)])))
