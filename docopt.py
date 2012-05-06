from ast import literal_eval
from copy import deepcopy
import sys
import re


class DocoptError(Exception):

    """Error in construction of usage-message by developer."""


class DocoptExit(SystemExit):

    """Exit in case user invoked program with incorect arguments."""

    usage = ''

    def __init__(self, message):
        SystemExit.__init__(self, message + '\n' + self.usage)


class Pattern(object):

    def __init__(self, *children):
        self.children = children

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__,
                           ', '.join(repr(a) for a in self.children))

    @property
    def flat(self):
        if not hasattr(self, 'children'):
            return [self]
        return sum([c.flat for c in self.children], [])


class Argument(Pattern):

    def __init__(self, meta, value=None):
        self.meta = meta
        self.value = value

    @property
    def name(self):
        return variabalize(self.meta.strip('<>').lower())

    def match(self, left, collected=None):
        collected = [] if collected is None else collected
        args = [l for l in left if type(l) == Argument]
        if not len(args):
            return False, left, collected
        left.remove(args[0])
        return True, left, collected + [Argument(self.meta, args[0].value)]

    def __repr__(self):
        return 'Argument(%r, %r)' % (self.meta, self.value)


class Option(Pattern):

    def __init__(self, short=None, long=None, value=False, parse=None):
        self.short = short
        self.long = long
        self.value = value

    def match(self, left, collected=None):
        collected = [] if collected is None else collected
        left_ = []
        for l in left:
            if not (type(l) == Option and
                    (self.short, self.long) == (l.short, l.long)):
                left_.append(l)
        return (left != left_), left_, collected

    @property
    def is_flag(self):
        if self.short:
            return not self.short.endswith(':')
        if self.long:
            return not self.long.endswith('=')

    @property
    def name(self):
        return variabalize((self.long or self.short).rstrip(':').rstrip('='))

    def __repr__(self):
        return 'Option(%r, %r, %r)' % (self.short, self.long, self.value)


class Required(Pattern):

    def match(self, left, collected=None):
        collected = [] if collected is None else collected
        c = []
        left = deepcopy(left)
        matched = True
        for p in self.children:
            m, left, c = p.match(left, c)
            if not m:
                matched = False
        return matched, left, (collected + c if matched else collected)


class Optional(Pattern):

    def match(self, left, collected=None):
        collected = [] if collected is None else collected
        left = deepcopy(left)
        for p in self.children:
            m, left, collected = p.match(left, collected)
        return True, left, collected


class OneOrMore(Pattern):

    def match(self, left, collected=None):
        collected = [] if collected is None else collected
        c = []
        assert len(self.children) == 1
        left_ = deepcopy(left)
        matched = True
        while matched:
            matched, left_, c = self.children[0].match(left_, c)
        # XXX: There could be that something below in hierarchy matched
        # but didn't lead to change in `left_`?
        matched = (left != left_)
        return matched, left_, (collected + c if matched else collected)


class Either(Pattern):

    def match(self, left, collected=None):
        collected = [] if collected is None else collected
        left = deepcopy(left)
        for p in self.children:
            matched, l, c = p.match(left, collected)
            if matched:
                return matched, l, c
        return False, left, collected


class Namespace(object):

    def __init__(self, **kw):
        self.__dict__ = kw

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return self.__dict__ != other.__dict__

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__,
                ',\n    '.join('%s=%r' % i for i in self.__dict__.items()))


class Options(Namespace):
    pass


class Arguments(Namespace):
    pass


def variabalize(s):
    ret = s[0] if s[0].isalpha() else '_'
    for ch in s[1:]:
        ret += ch if ch.isalpha() or ch.isdigit() else '_'
    return ret


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
        raise DocoptExit('--%s is not recognized' % raw)
    if len(opt) > 1:
        raise DocoptExit('--%s is not a unique prefix: %s?' % (raw,
                ', '.join('--%s' % o.long for o in opt)))
    opt = opt[0]
    if not opt.is_flag:
        if value is None:
            if not parse:
                raise DocoptExit('--%s requires argument' % opt)
            value, parse = parse[0], parse[1:]
    elif value is not None:
        raise DocoptExit('--%s must not have an argument' % opt)
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
                    raise DocoptExit('opt -%s requires argument' % opt)
                raw, parse = parse[0], parse[1:]
            value, raw = raw, ''
        opt.value = value
        parsed += [opt]
    return parsed, parse


def split(a, sep='|'):
    if sep in a:
        return [a[:a.index(sep)]] + split(a[a.index(sep) + 1:], sep)
    return [a]


def matching_paren(a):
    left = a[0]
    right = '[]()'['[]()'.index(left) + 1]
    count = 0
    for i, v in enumerate(a):
        if v == left:
            count += 1
        elif v == right:
            count -= 1
        if count == 0:
            return i
    raise DocoptError('Unbalanced parenthesis or brackets in usage-pattern.')


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
        if is_pattern and source[0] == '[':
            matching = matching_paren(source)
            sub_parse = source[1:matching]
            parsed += [Optional(*parse(sub_parse, is_pattern=is_pattern,
                                       options=options))]
            source = source[matching + 1:]
        elif is_pattern and source[0] == '(':
            matching = matching_paren(source)
            sub_parse = source[1:matching]
            parsed += [Required(*parse(sub_parse, is_pattern=is_pattern,
                                       options=options))]
            source = source[matching + 1:]
        elif is_pattern and '|' in source:
            either = []
            for s in split(source, '|'):
                p = parse(s, is_pattern=is_pattern, options=options)
                either += p if len(p) == 1 else [Required(*p)]
            assert parsed == []
            parsed = [Either(*either)]
            break
        elif is_pattern and source[0] == '...':
            parsed[-1] = OneOrMore(parsed[-1])
            source = source[1:]
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
            a = Argument(source[0]) if is_pattern else Argument(None, source[0])
            parsed += [a]
            source = source[1:]
    return parsed


def parse_doc_options(doc):
    return [option('-' + s) for s in re.split('^ *-|\n *-', doc)[1:]]


def usage(doc):
    return re.split(r'\n\s*\n', ''.join(re.split(r'([Uu]sage:)',
                    doc)[1:3]))[0].strip()


def parse_doc_usage(doc, options=[]):
    raw_usage = re.split(r'\n\s*\n', re.split(r'[Uu]sage:', doc)[1])[0].strip()
    prog = raw_usage.split()[0]
    raw_patterns = raw_usage.strip(prog).split(prog)
    return [p.strip() for p in raw_patterns]


def extras(help, version, options, doc):
    if help and any(o for o in options
            if (o.short == 'h' or o.long == 'help') and o.value):
        print(doc.strip())
        exit()
    if version and any(o for o in options if o.long == 'version' and o.value):
        print(version)
        exit()


def docopt(doc, args=sys.argv[1:], help=True, version=None):
    DocoptExit.usage = usage(doc)
    options = parse_doc_options(doc)
    args = parse(args, options=options)
    overlapped = options + [o for o in args if type(o) is Option]
    extras(help, version, overlapped, doc)
    patterns = []
    for raw_pattern in parse_doc_usage(doc):
        p = Required(*pattern(raw_pattern, options=options))
        patterns.append(p)
    flats = sum([p.flat for p in patterns], [])
    pot_arguments = [a for a in flats if type(a) is Argument]
    for p in patterns:
        matched, left, collected = p.match(args)
        if matched and left == []:
            return (Options(**dict([(o.name, o.value) for o in overlapped])),
                  Arguments(**dict([(a.name, a.value)
                            for a in pot_arguments + collected])))
    raise DocoptExit('did not match usage')
