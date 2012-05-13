from ast import literal_eval
from copy import deepcopy
import sys
import re


class DocoptError(Exception):

    """Error in construction of usage-message by developer."""


class DocoptExit(SystemExit):

    """Exit in case user invoked program with incorect arguments."""

    usage = ''

    def __init__(self, message=''):
        SystemExit.__init__(self, (message + '\n' + self.usage).strip())


class Pattern(object):

    def __init__(self, *children):
        self.children = list(children)

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __hash__(self):
        return hash(repr(self))

#   def __ne__(self, other):
#       return repr(self) == repr(other)

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__,
                           ', '.join(repr(a) for a in self.children))

    @property
    def flat(self):
        if not hasattr(self, 'children'):
            return [self]
        return sum([c.flat for c in self.children], [])

    def fix(self):
        self.fix_identities()
        self.fix_list_arguments()
        return self

    def fix_identities(self, uniq=None):
        """Make pattern-tree tips point to same object if they are equal."""
        if not hasattr(self, 'children'):
            return self
        uniq = list(set(self.flat)) if uniq == None else uniq
        for i, c in enumerate(self.children):
            if not hasattr(c, 'children'):
                assert c in uniq
                self.children[i] = uniq[uniq.index(c)]
            else:
                c.fix_identities(uniq)

    def fix_list_arguments(self):
        """Find arguments that should accumulate values and fix them."""
        either = [list(c.children) for c in self.either.children]
        for case in either:
            case = [c for c in case if case.count(c) > 1]
            for a in [e for e in case if type(e) == Argument]:
                a.value = []
        return self

    @property
    def either(self):
        """Transform pattern into an equivalent, with only top-level Either."""
        # Currently the pattern will not be equivalent, but more "narrow",
        # although good enough to reason about list arguments.
        if not hasattr(self, 'children'):
            return Either(Required(self))
        else:
            ret = []
            groups = [[self]]
            while groups:
                children = groups.pop(0)
                types = [type(c) for c in children]
                if Either in types:
                    either = [c for c in children if type(c) == Either][0]
                    children.pop(children.index(either))
                    for c in either.children:
                        groups.append([c] + children)
                elif Required in types:
                    required = [c for c in children if type(c) == Required][0]
                    children.pop(children.index(required))
                    groups.append(list(required.children) + children)
                elif Optional in types:
                    optional = [c for c in children if type(c) == Optional][0]
                    children.pop(children.index(optional))
                    groups.append(list(optional.children) + children)
                elif OneOrMore in types:
                    oneormore = [c for c in children if type(c) == OneOrMore][0]
                    children.pop(children.index(oneormore))
                    groups.append(list(oneormore.children) * 2 + children)
                else:
                    ret.append(children)
            return Either(*[Required(*e) for e in ret])


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
        if type(self.value) is not list:
            return True, left, collected + [Argument(self.meta, args[0].value)]
        same_meta = [a for a in collected
                     if type(a) == Argument and a.meta == self.meta]
        if len(same_meta):
            same_meta[0].value += [args[0].value]
            return True, left, collected
        else:
            return True, left, collected + [Argument(self.meta,
                                                     [args[0].value])]

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
            # if this is so greedy, how to handle OneOrMore then?
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
        times = 0
        while matched:
            # could it be that something didn't match but changed left_ or c?
            matched, left_, c = self.children[0].match(left_, c)
            times += 1 if matched else 0
        matched = (times >= 1)
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
        matched = re.findall('\[default: (.*)\]', description, flags=re.I)
        value = argument_eval(matched[0]) if matched else False
        short = short + ':' if short else None
        long = long + '=' if long else None
    return Option(short, long, value)


def argument_eval(s):
    try:
        return literal_eval(s)
    except (ValueError, SyntaxError):
        return s


def do_longs(parsed, raw, options, parse, is_pattern):
    try:
        i = raw.index('=')
        raw, value = raw[:i], raw[i + 1:]
    except ValueError:
        value = None
    opt = [o for o in options if o.long and o.long.startswith(raw)]
    if len(opt) < 1:
        if is_pattern:
            raise DocoptError('--%s in "usage" should be '
                              'mentioned in option-description' % raw)
        raise DocoptExit('--%s is not recognized' % raw)
    if len(opt) > 1:
        if is_pattern:
            raise DocoptError('--%s in "usage" is not a unique prefix: %s?' %
                              (raw, ', '.join('--%s' % o.long for o in opt)))
        raise DocoptExit('--%s is not a unique prefix: %s?' %
                         (raw, ', '.join('--%s' % o.long for o in opt)))
    opt = opt[0]
    if not opt.is_flag:
        if value is None:
            if not parse:
                if is_pattern:
                    raise DocoptError('--%s in "usage" requires argument' %
                                      opt.name)
                raise DocoptExit('--%s requires argument' % opt.name)
            value, parse = parse[0], parse[1:]
    elif value is not None:
        if is_pattern:
            raise DocoptError('--%s in "usage" must not have an argument' %
                             opt.name)
        raise DocoptExit('--%s must not have an argument' % opt.name)
    opt.value = value or True
    parsed += [opt]
    return parsed, parse


def do_shorts(parsed, raw, options, parse, is_pattern):
    while raw != '':
        opt = [o for o in options if o.short and o.short.startswith(raw[0])]
        if len(opt) > 1:
            raise DocoptError('-%s is specified ambiguously %d times' %
                              (raw[0], len(opt)))
        if len(opt) < 1:
            if is_pattern:
                raise DocoptError('-%s in "usage" should be mentioned '
                                  'in option-description' % raw[0])
            raise DocoptExit('-%s is not recognized' % raw[0])
        assert len(opt) == 1
        opt = opt[0]
        raw = raw[1:]
        if opt.is_flag:
            value = True
        else:
            if raw == '':
                if not parse:
                    if is_pattern:
                        raise DocoptError('-%s in "usage" requires argument' %
                                          opt.short[0])
                    raise DocoptExit('-%s requires argument' % opt.short[0])
                raw, parse = parse[0], parse[1:]
            value, raw = raw, ''
        opt.value = value
        parsed += [opt]
    return parsed, parse


def split_simple(a, sep='|'):
    if sep in a:
        return [a[:a.index(sep)]] + split_simple(a[a.index(sep) + 1:], sep)
    return [a]


def split_either(a, sep='|'):
    a = deepcopy(a)
    count_b = count_p = 0
    for i, v in enumerate(a):
        if v == '[':
            count_b += 1
        elif v == ']':
            count_b -= 1
        elif v == '(':
            count_p += 1
        elif v == ')':
            count_p -= 1
        elif v == '|' and count_b == count_p == 0:
            a[i] = '@'
    return split_simple(a, '@')


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
    options = [] if options is None else deepcopy(options)
    if type(source) == str:
        source = re.sub(r'([\[\]\(\)\|]|\.\.\.)', r' \1 ', source).split()
    tokens = '[ ] ( ) | ...'.split()
    parsed = []
    while source:
        if '|' in source and len(split_either(source)) > 1:
            either = []
            for s in split_either(source, '|'):
                p = pattern(s, options=options)
                either += [p.children[0]] if len(p.children) == 1 else [p]
            assert parsed == []
            parsed = [Either(*either)]
            break
        elif source[0] == '[':
            matching = matching_paren(source)
            sub_parse = source[1:matching]
            parsed += [Optional(*pattern(sub_parse, options=options).children)]
            source = source[matching + 1:]
        elif source[0] == '(':
            matching = matching_paren(source)
            sub_parse = source[1:matching]
            parsed += [pattern(sub_parse, options=options)]
            source = source[matching + 1:]
        elif source[0] == '...':
            parsed[-1] = OneOrMore(parsed[-1])
            source = source[1:]
        else:
            i = min([source.index(t) for t in tokens if t in source]
                    + [len(source)])
            parsed += parse(source[:i], options=options, is_pattern=True)
            source = source[i:]
    return Required(*parsed)


def parse(source, options=None, is_pattern=False):
    options = [] if options is None else deepcopy(options)
    source = source.split() if type(source) == str else source
    parsed = []
    while source:
        if source[0] == '--':
            parsed += [Argument(None, v) for v in source[1:]]
            break
        elif source[0][:2] == '--':
            parsed, source = do_longs(parsed, source[0][2:],
                                      options, source[1:], is_pattern)
        elif source[0][:1] == '-' and source[0] != '-':
            parsed, source = do_shorts(parsed, source[0][1:],
                                       options, source[1:], is_pattern)
        else:
            parsed.append(Argument(source[0]) if is_pattern
                          else Argument(None, source[0]))
            source = source[1:]
    return parsed


def parse_doc_options(doc):
    return [option('-' + s) for s in re.split('^ *-|\n *-', doc)[1:]]


def printable_usage(doc):
    return re.split(r'\n\s*\n',
                    ''.join(re.split(r'(usage:)', doc, flags=re.I)[1:])
                   )[0].strip()


def formal_usage(printable_usage):
    pu = printable_usage.split()[1:]  # split and drop "usage:"
    prog = pu[0]
    return ' '.join(['|' if s == prog else s for s in pu[1:]])


def extras(help, version, options, doc):
    if help and any(o for o in options
            if (o.short == 'h' or o.long == 'help') and o.value):
        print(doc.strip())
        exit()
    if version and any(o for o in options if o.long == 'version' and o.value):
        print(version)
        exit()


def docopt(doc, args=sys.argv[1:], help=True, version=None):
    DocoptExit.usage = docopt.usage = printable_usage(doc)
    options = parse_doc_options(doc)
    args = parse(args, options=options)
    overlapped = options + [o for o in args if type(o) is Option]
    extras(help, version, overlapped, doc)
    formal_pattern = pattern(formal_usage(DocoptExit.usage), options=options)
    pot_arguments = [a for a in formal_pattern.flat if type(a) is Argument]
    matched, left, collected = formal_pattern.fix().match(args)
    if matched and left == []:  # is checking left needed here?
        return (Options(**dict([(o.name, o.value) for o in overlapped])),
              Arguments(**dict([(a.name, a.value)
                        for a in pot_arguments + collected])))
    raise DocoptExit()
