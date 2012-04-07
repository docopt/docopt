'''Quick & Dirty (TM)'''
import sys
import re
from inspect import cleandoc
from ast import literal_eval


def _parse_single_description(s):
    forms = re.split('\s\s', s)[0].replace(',', ' ')
    has_arg = '=' in forms
    forms = forms.replace('=', ' ')
    if '--' in forms:
        full = re.findall('--(\S+)', forms)[0]
        rest = forms.split('--')[0]
    else:
        full = None
        rest = forms
    if '-' in rest:
        short = re.findall('-(\S)', rest)[0]
    else:
        short = None
    if 'efault: ' in s:
        has_default = True
        default = _eval_arg(re.findall('efault:\s*(\S+)[\s\)\]].*', s)[0])
    else:
        has_default = False
        default = None
    #entry = {'short': short, 'full': full, 'has_arg': has_arg,
    #         'has_default': has_default, 'default': default}
    return short, full, has_arg, has_default, default


def _eval_arg(s):
    try:
        return literal_eval(s)
    except:
        return s

def _variabalize(s):
    ret = s[0] if s[0].isalpha() else '_'
    for ch in s[1:]:
        ret += ch if ch.isalpha() or ch.isdigit() else '_'
    return ret


class _FormalOption(object):
    def __init__(self, description):
        (self.short,
        self.full,
        self.has_arg,
        self.has_default,
        self.default) = _parse_single_description(description)
        self.name = _variabalize(self.full or self.short)
        self.value = None


def _parse_description(s):
    s = cleandoc(s)
    par = []
    for line in ['-' + l for l in re.split('\n\s*-', s)[1:]]:
        par.append(_FormalOption(line))
    return par


class _FormalOptionCollection(object):
    def __init__(self, description):
        self._d = _parse_description(description)
    def __iter__(self):
        return iter(self._d)
    def match(self, s):
        for o in self._d:
            if o.short and '-' + o.short == s:
                return o
            if o.full and '--' + o.full == s:
                return o
        return None


def _normalize_args(argv):
    argv = ' '.join(argv).replace('=', ' ').split(' ')
    ret = []
    for a in argv:
        if a.startswith('-') and not a.startswith('--'):
            ret += ['-' + c for c in list(a[1:])]
        else:
            ret += [a]
    return ret


def _split_options_and_arguments(argv, formal_options):
    argv = _normalize_args(argv)[1:]
    opt = []
    arg = []
    for i in reversed(range(len(argv))):
        if argv[i].startswith('-'):
            for o in formal_options:
                if o.short and argv[i] == '-' + o.short or \
                   o.full and argv[i] == '--' + o.full:
                    if o.has_arg:
                        opt = argv[:i + 2]
                        arg = argv[i + 2:]
                        break
            if not (opt or arg):
                opt = argv[:i + 1]
                arg = argv[i + 1:]
            break
    return opt, arg


class Bunch(object):
    def __init__(self, **kw):
        self.__dict__ = kw


def _group_options(opt):
    '''Works on normalized only.'''
    return [('-' + g).split(' ') for g in (' ' + ' '.join(opt)).split(' -')[1:]]


def _parse_options(opt, formal_options):
    bunch = dict((o.name, False) for o in formal_options)
    opt = _group_options(opt)
    for o in opt:
        m = formal_options.match(o[0])
        if not m:
            print 'unknown option:', o[0]
        else:
            if (len(o) == 1 and not m.has_arg):
                bunch[m.name] = True
            elif (len(o) == 2 and m.has_arg):
                bunch[m.name] = _eval_arg(o[1])
            else:
                print 'wrong arguments:', ' '.join(o)
    return bunch


def _parse_arguments(arg):
    '''No argument parsing at the moment.'''
    return arg


def parse_options_and_arguments(description, argv=sys.argv):
    foc = _FormalOptionCollection(description)
    opt, arg = _split_options_and_arguments(argv, foc)
    opt = _parse_options(opt)
    arg = _parse_arguments(arg)
    return opt, arg

