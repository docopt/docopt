from copy import copy
import sys
import re


class DocoptError(Exception):

    """Error in construction of usage-message by developer."""


class DocoptExit(SystemExit):

    """Exit in case user invoked program with incorrect arguments."""

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

    def __ne__(self, other):
        return repr(self) == repr(other)

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
                    either = [c for c in children if type(c) is Either][0]
                    children.pop(children.index(either))
                    for c in either.children:
                        groups.append([c] + children)
                elif Required in types:
                    required = [c for c in children if type(c) is Required][0]
                    children.pop(children.index(required))
                    groups.append(list(required.children) + children)
                elif Optional in types:
                    optional = [c for c in children if type(c) is Optional][0]
                    children.pop(children.index(optional))
                    groups.append(list(optional.children) + children)
                elif OneOrMore in types:
                    oneormore = [c for c in children if type(c) is OneOrMore][0]
                    children.pop(children.index(oneormore))
                    groups.append(list(oneormore.children) * 2 + children)
                else:
                    ret.append(children)
            return Either(*[Required(*e) for e in ret])


class Argument(Pattern):

    def __init__(self, meta, value=None):
        self.meta = meta
        self.value = value

    def match(self, left, collected=None):
        collected = [] if collected is None else collected
        args = [l for l in left if type(l) is Argument]
        if not len(args):
            return False, left, collected
        left.remove(args[0])
        if type(self.value) is not list:
            return True, left, collected + [Argument(self.meta, args[0].value)]
        same_meta = [a for a in collected
                     if type(a) is Argument and a.meta == self.meta]
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
            if not (type(l) is Option and
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
        return ('--' + self.long.rstrip('=') if self.long
                else '-' + self.short.rstrip(':'))

    def __repr__(self):
        return 'Option(%r, %r, %r)' % (self.short, self.long, self.value)

class AnyOptions(Pattern):

    def match(self, left, collected=None):
        collected = [] if collected is None else collected
        left_ = [l for l in left if not type(l) == Option]
        return (left != left_), left_, collected

class Required(Pattern):

    def match(self, left, collected=None):
        collected = [] if collected is None else collected
        l = copy(left)
        c = copy(collected)
        for p in self.children:
            matched, l, c = p.match(l, c)
            if not matched:
                return False, left, collected
        return True, l, c


class Optional(Pattern):

    def match(self, left, collected=None):
        collected = [] if collected is None else collected
        left = copy(left)
        for p in self.children:
            m, left, collected = p.match(left, collected)
        return True, left, collected


class OneOrMore(Pattern):

    def match(self, left, collected=None):
        assert len(self.children) == 1
        collected = [] if collected is None else collected
        l = copy(left)
        c = copy(collected)
        l_ = None
        matched = True
        times = 0
        while matched:
            # could it be that something didn't match but changed l or c?
            matched, l, c = self.children[0].match(l, c)
            times += 1 if matched else 0
            if l_ == l:
                break
            l_ = copy(l)
        if times >= 1:
            return True, l, c
        return False, left, collected


class Either(Pattern):

    def match(self, left, collected=None):
        collected = [] if collected is None else collected

        outcomes = []
        for p in self.children:
            matched, _, _ = outcome = p.match(copy(left), copy(collected))
            if matched:
                outcomes.append(outcome)

        if outcomes:
            return min(outcomes, key=lambda outcome: len(outcome[1]))

        return False, left, collected


def option(full_description):
    is_flag = True
    short, long, value = None, None, False
    options, _, description = full_description.strip().partition('  ')
    options = options.replace(',', ' ').replace('=', ' ')
    for s in options.split():
        if s.startswith('--'):
            long = s.lstrip('-')
        elif s.startswith('-'):
            short = s.lstrip('-')
        else:
            is_flag = False
    if not is_flag:
        matched = re.findall('\[default: (.*)\]', description, flags=re.I)
        value = matched[0] if matched else False
        short = short + ':' if short else None
        long = long + '=' if long else None
    return Option(short, long, value)


class TokenStream(object):

    def __init__(self, iterable):
        self.i = iterable

    def __iter__(self):
        return iter(self.i)

    def pop(self, default=None):
        return self.i.pop(0) if len(self.i) else default

    def peek(self, default=None):
        return self.i[0] if len(self.i) else default


def do_long(raw, options, tokens, is_pattern):
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
    opt = copy(opt[0])
    if not opt.is_flag:
        if value is None:
            if not tokens.peek():
                if is_pattern:
                    raise DocoptError('--%s in "usage" requires argument' %
                                      opt.name)
                raise DocoptExit('--%s requires argument' % opt.name)
            value = tokens.pop()
    elif value is not None:
        if is_pattern:
            raise DocoptError('--%s in "usage" must not have an argument' %
                             opt.name)
        raise DocoptExit('--%s must not have an argument' % opt.name)
    opt.value = value or True
    return opt


def do_shorts(raw, options, tokens, is_pattern):
    parsed = []
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
        opt = copy(opt[0])
        raw = raw[1:]
        if opt.is_flag:
            value = True
        else:
            if raw == '':
                if not tokens.peek():
                    if is_pattern:
                        raise DocoptError('-%s in "usage" requires argument' %
                                          opt.short[0])
                    raise DocoptExit('-%s requires argument' % opt.short[0])
                raw = tokens.pop()
            value, raw = raw, ''
        opt.value = value
        parsed += [opt]
    return parsed

def parse_pattern(source, options):
    tokens = re.sub(r'([\[\]\(\)\|]|\.\.\.)', r' \1 ', source).split()
    tokens = TokenStream(tokens)
    result = parse_expr(tokens, options)
    assert not tokens.peek()
    return Required(*result)


# Usage string grammar:
#   EXPR ::= SEQ ("|" SEQ)*
#   SEQ  ::= (ATOM ["..."])*
#   ATOM ::= LONG | SHORTS (plural!) | ARG | "[" EXPR "]" | "(" EXPR ")"
#
# Note [] behavior:
#   [-a -b] is equivalent to [-a] [-b], not [(-a -b)]
# This is why all these parse_ functions return lists.

def parse_expr(tokens, options):
    """EXPR ::= SEQ ('|' SEQ)*"""
    seq = parse_seq(tokens, options)

    if not tokens.peek() or tokens.peek() != '|':
        return seq

    if len(seq) > 1:
        seq = [Required(*seq)]
    result = seq
    while tokens.peek() and tokens.peek() == '|':
        tokens.pop()
        seq = parse_seq(tokens, options)
        result += [Required(*seq)] if len(seq) > 1 else seq

    if len(result) == 1:
        return result
    return [Either(*result)]


def parse_seq(tokens, options):
    """SEQ ::= (ATOM ['...'])*"""
    result = []
    while True:
        if not tokens.peek() or tokens.peek() in [']', ')', '|']:
            break

        atom = parse_atom(tokens, options)

        if tokens.peek() and tokens.peek() == '...':
            tokens.pop()
            atom, = atom
            atom = [OneOrMore(atom)]

        result += atom

    return result


def parse_atom(tokens, options):
    """ATOM ::=
        LONG | SHORTS (plural!) | ANYOPTIONS
        | ARG | '[' EXPR ']' | '(' EXPR ')'
    """
    token = tokens.pop()
    result = []
    if token == '(':
        result = [Required(*parse_expr(tokens, options))]
        token = tokens.pop(default='EOF')
        if token != ')':
            raise DocoptError("Unmatched '('")
        return result
    elif token == '[':
        if tokens.peek() == 'options':
            result = [Optional(AnyOptions())]
            tokens.pop()
        else:
            result = [Optional(*parse_expr(tokens, options))]
        token = tokens.pop(default='EOF')
        if token != ']':
            raise DocoptError("Unmatched '['")
        return result
    elif token == '--':
        raise DocoptError("'--' in usage string is not supported")
    elif token.startswith('--'):
        return [do_long(token[2:], options, tokens, is_pattern=True)]
    elif token.startswith('-'):
        return do_shorts(token[1:], options, tokens, is_pattern=True)
    else:
        return [Argument(token)]


def parse_args(source, options):
    if type(source) is str:
        source = source.split()
    tokens = TokenStream(source)
    options = copy(options)
    parsed = []
    while tokens.peek():
        token = tokens.pop()
        if token == '--':
            parsed += [Argument(None, v) for v in tokens]
            break
        elif token.startswith('--'):
            parsed += [do_long(token[2:], options, tokens, is_pattern=False)]
        elif token.startswith('-') and token != '-':
            parsed += do_shorts(token[1:], options, tokens, is_pattern=False)
        else:
            parsed.append(Argument(None, token))
    return parsed


def parse_doc_options(doc):
    return [option('-' + s) for s in re.split('^ *-|\n *-', doc)[1:]]


def printable_usage(doc):
    return re.split(r'\n\s*\n',
                    ''.join(re.split(r'([Uu][Ss][Aa][Gg][Ee]:)', doc)[1:])
                   )[0].strip()


def formal_usage(printable_usage):
    pu = printable_usage.split()[1:]  # split and drop "usage:"
    prog = pu[0]
    return ' '.join('|' if s == prog else s for s in pu[1:])


def extras(help, version, options, doc):
    if help and any((o.short == 'h' or o.long == 'help') and o.value
                    for o in options):
        print(doc.strip())
        exit()
    if version and any(o.long == 'version' and o.value for o in options):
        print(version)
        exit()


class Dict(dict):
    def __repr__(self):
        return '{%s}' % ',\n '.join('%r: %r' % i for i in sorted(self.items()))


def docopt(doc, argv=sys.argv[1:], help=True, version=None):
    DocoptExit.usage = docopt.usage = printable_usage(doc)
    options = parse_doc_options(doc)
    argv = parse_args(argv, options=options)
    overlapped = options + [o for o in argv if type(o) is Option]
    extras(help, version, overlapped, doc)
    formal_pattern = parse_pattern(formal_usage(docopt.usage), options=options)
    pot_arguments = [a for a in formal_pattern.flat if type(a) is Argument]
    matched, left, collected = formal_pattern.fix().match(argv)
    if matched and left == []:  # better message if left?
        return Dict(list(dict((o.name, o.value) for o in overlapped).items()) +
                    list(dict((a.meta, a.value) for a in
                              pot_arguments + collected).items()))
    raise DocoptExit()
