# Python 2 Cleanup Analysis for docopt

## Executive Summary

This document identifies Python 2-specific code, compatibility shims that can be removed for Python 3.10+, and dead/unused code paths in the docopt codebase.

---

## 1. Python 2-Specific Code

### 1.1 Explicit Python 2 Syntax

#### `test_docopt.py:1` - `from __future__ import with_statement`
```1:1:test_docopt.py
from __future__ import with_statement
```
**Status**: REMOVABLE  
**Reason**: `with_statement` was required in Python 2.5. It's been standard since Python 2.6+ and is always available in Python 3.0+.

#### `test_docopt.py:444-449` - Unicode string literal test
```444:449:test_docopt.py
def test_issue34_unicode_strings():
    try:
        assert docopt(eval("u'usage: prog [-o <a>]'"), '') == \
                {'-o': False, '<a>': None}
    except SyntaxError:
        pass  # Python 3
```
**Status**: REMOVABLE  
**Reason**: The `u'...'` prefix is Python 2-specific. In Python 3, all strings are Unicode by default, and `u'...'` syntax was removed in Python 3.0-3.2, then re-added in 3.3+ for compatibility but is unnecessary. For Python 3.10+, this entire test can be simplified or removed.

#### `docopt.py:32` - Old-style class inheritance
```32:32:docopt.py
class Pattern(object):
```
**Status**: REMOVABLE (but harmless)  
**Reason**: `class Pattern(object):` is Python 2-style explicit inheritance. In Python 3, `class Pattern:` is equivalent. However, this is harmless and doesn't break anything.

#### `conftest.py:51` - Old-style super() call
```51:51:conftest.py
        super(DocoptTestItem, self).__init__(name, parent)
```
**Status**: REMOVABLE  
**Reason**: Python 3 allows `super()` without arguments. Can be changed to `super().__init__(name, parent)`.

### 1.2 Python 2 Compatibility Shims

#### `conftest.py:2-5` - simplejson fallback
```2:5:conftest.py
try:
    import json
except ImportError:
    import simplejson as json
```
**Status**: REMOVABLE  
**Reason**: `json` module has been in the standard library since Python 2.6. `simplejson` was only needed for Python 2.5 and earlier. For Python 3.10+, this fallback is unnecessary.

#### `examples/config_file_example.py:22-27` - ConfigParser/StringIO compatibility
```22:27:examples/config_file_example.py
    try:  # Python 2
        from ConfigParser import ConfigParser
        from StringIO import StringIO
    except ImportError:  # Python 3
        from configparser import ConfigParser
        from io import StringIO
```
**Status**: REMOVABLE (in example file)  
**Reason**: This is in an example file, not core code. For Python 3.10+, can use only the Python 3 imports.

#### `examples/config_file_example.py:44` - readfp() method
```44:44:examples/config_file_example.py
    config.readfp(config_file)
```
**Status**: REMOVABLE  
**Reason**: `readfp()` was deprecated in Python 3.2 and removed in Python 3.12. Should use `read_file()` instead (available since Python 3.2).

#### `docopt.py:285` - hasattr check for split()
```285:285:docopt.py
        self += source.split() if hasattr(source, 'split') else source
```
**Status**: QUESTIONABLE  
**Reason**: This check allows `Tokens` to accept both strings and lists. In Python 3.10+, if we're only supporting strings, this can be simplified. However, this might be intentional API design to accept lists. Needs verification of intended behavior.

### 1.3 Python 2-Style Dictionary Constructors

#### `examples/config_file_example.py:49, 60` - dict() with generator expressions
```49:49:examples/config_file_example.py
    return dict((key, True if value is None else value)
```
```60:60:examples/config_file_example.py
    return dict((str(key), dict_1.get(key) or dict_2.get(key))
```
**Status**: STYLE ONLY (not Python 2-specific)  
**Reason**: `dict((k, v) for ...)` works in both Python 2 and 3. Modern Python 3 style prefers `{k: v for ...}` but this is not Python 2-specific code.

---

## 2. Compatibility Shims Removable for Python 3.10+

### 2.1 Test Infrastructure

#### `conftest.py:38, 42, 76` - pytest.fspath API
```38:38:conftest.py
        raw = self.fspath.open().read()
```
```42:42:conftest.py
            name = self.fspath.purebasename
```
```76:76:conftest.py
        return self.fspath, 0, "usecase: %s" % self.name
```
**Status**: NEEDS UPDATE  
**Reason**: `fspath` is a deprecated pytest API (py.path.local). Modern pytest uses `pathlib.Path`. The `fspath` attribute was deprecated in pytest 7.0 and may be removed in future versions. Should migrate to `pathlib.Path` API.

### 2.2 String Formatting

#### `docopt.py:358` - Old-style % formatting
```358:358:docopt.py
                        raise tokens.error('%s requires argument' % short)
```
**Status**: STYLE ONLY (not required)  
**Reason**: `%` formatting works fine in Python 3.10+, but modern style prefers f-strings or `.format()`. Not a compatibility issue, just style.

#### `conftest.py:44, 70` - Old-style % formatting
```44:44:conftest.py
                yield DocoptTestItem("%s(%d)" % (name, index), self, doc, case)
```
```70:70:conftest.py
                "$ %s %s" % (self.prog, self.argv),
```
**Status**: STYLE ONLY (not required)  
**Reason**: Same as above - works but could be modernized.

---

## 3. Dead or Unused Code Paths

### 3.1 Commented-Out Code Blocks

#### `docopt.py:564-568` - Disabled argument default parsing
```564:568:docopt.py
    # [default] syntax for argument is disabled
    #for a in pattern.flat(Argument):
    #    same_name = [d for d in arguments if d.name == a.name]
    #    if same_name:
    #        a.value = same_name[0].value
```
**Status**: DEAD CODE  
**Reason**: Entirely commented out. If this feature is not planned, should be removed. If it's planned for future, should have a TODO/FIXME comment explaining why it's disabled.

#### `docopt.py:574-576` - Commented any_options feature
```574:576:docopt.py
        #if any_options:
        #    options_shortcut.children += [Option(o.short, o.long, o.argcount)
        #                    for o in argv if type(o) is Option]
```
**Status**: DEAD CODE  
**Reason**: Commented out code referencing `any_options` parameter that doesn't exist in the function signature. This appears to be leftover from a removed feature.

#### `test_docopt.py:341-344` - Commented test cases
```341:344:test_docopt.py
#    with raises(DocoptLanguageError):
#        docopt('Usage: prog --non-existent', '--non-existent')
#    with raises(DocoptLanguageError):
#        docopt('Usage: prog --non-existent')
```
**Status**: DEAD CODE  
**Reason**: Commented-out tests. Either remove or uncomment if these are valid test cases.

#### `test_docopt.py:364-365` - Commented test case
```364:365:test_docopt.py
#    with raises(DocoptLanguageError):
#        docopt('Usage: prog -x')
```
**Status**: DEAD CODE  
**Reason**: Same as above.

#### `test_docopt.py:426-427` - Commented test with XXX
```426:427:test_docopt.py
    #with raises(SystemExit):
    #    docopt(doc, 'help')  XXX Maybe help command?
```
**Status**: DEAD CODE  
**Reason**: Commented test with unclear intent. Should be removed or clarified.

#### `test_docopt.py:467-481` - Commented any_options tests
```467:481:test_docopt.py
#    assert docopt('usage: prog [options]', '-foo --bar --spam=eggs',
#                  any_options=True) == {'-f': True, '-o': 2,
#                                         '--bar': True, '--spam': 'eggs'}
#    with raises(DocoptExit):
#        docopt('usage: prog [options]', '--foo --bar --bar')
#    assert docopt('usage: prog [options]', '--foo --bar --bar',
#                  any_options=True) == {'--foo': True, '--bar': 2}
#    with raises(DocoptExit):
#        docopt('usage: prog [options]', '--bar --bar --bar -ffff')
#    assert docopt('usage: prog [options]', '--bar --bar --bar -ffff',
#                  any_options=True) == {'--bar': 3, '-f': 4}
#    with raises(DocoptExit):
#        docopt('usage: prog [options]', '--long=arg --long=another')
#    assert docopt('usage: prog [options]', '--long=arg --long=another',
#                  any_options=True) == {'--long': ['arg', 'another']}
```
**Status**: DEAD CODE  
**Reason**: Multiple commented tests referencing `any_options=True` parameter that doesn't exist. These are remnants of a removed feature.

#### `test_docopt.py:484-489` - Commented any_options test function
```484:489:test_docopt.py
#def test_options_shortcut_multiple_commands():
#    # any_options is disabled
#    assert docopt('usage: prog c1 [options] prog c2 [options]',
#        'c2 -o', any_options=True) == {'-o': True, 'c1': False, 'c2': True}
#    assert docopt('usage: prog c1 [options] prog c2 [options]',
#        'c1 -o', any_options=True) == {'-o': True, 'c1': True, 'c2': False}
```
**Status**: DEAD CODE  
**Reason**: Entire commented function for removed feature.

#### `test_docopt.py:510-529` - Commented parse_defaults test
```510:529:test_docopt.py
#def test_parse_defaults():
#    assert parse_defaults("""usage: prog
#                          options:
#                          -o, --option <o>
#                          --another <a>  description
#                                         [default: x]
#                          <a>
#                          <another>  description [default: y]""") == \
#           ([Option('-o', '--option', 1, None),
#             Option(None, '--another', 1, 'x')],
#            [Argument('<a>', None),
#             Argument('<another>', 'y')])
#
#    doc = '''
#    -h, --help  Print help message.
#    -o FILE     Output file.
#     --verbose   Verbose mode.'''
#    assert parse_defaults(doc)[0] == [Option('-h', '--help'),
#                                      Option('-o', None, 1),
#                                      Option(None, '--verbose')]
```
**Status**: DEAD CODE  
**Reason**: Commented test function. Should be removed or uncommented if valid.

### 3.2 Unused Variables/Imports

#### `docopt.py:455` - FIXME comment
```455:455:docopt.py
        # FIXME corner case "bla: options: --foo"
```
**Status**: DOCUMENTATION  
**Reason**: Not dead code, but a TODO/FIXME that should be addressed or removed if no longer relevant.

#### `test_docopt.py:387` - FIXME comment
```387:387:test_docopt.py
    with raises(DocoptExit):  # "--" is not allowed; FIXME?
```
**Status**: DOCUMENTATION  
**Reason**: FIXME comment suggesting uncertainty about behavior. Should be clarified or removed.

### 3.3 Configuration Files Referencing Python 2

#### `setup.py:36-37` - Python 2 classifiers
```36:37:setup.py
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
```
**Status**: REMOVABLE  
**Reason**: If targeting Python 3.10+, these classifiers should be removed.

#### `tox.ini:7` - Python 2 test environments
```7:7:tox.ini
envlist = py27, py34, py35, py36
```
**Status**: REMOVABLE  
**Reason**: `py27` should be removed. Also `py34`, `py35`, `py36` are EOL. For Python 3.10+, should update to `py310, py311, py312, py313`.

#### `tox.ini:13-16` - Python 2.7 specific testenv
```13:16:tox.ini
[testenv:py27]
commands = py.test
           py.test --doctest-modules docopt.py
deps = pytest
```
**Status**: REMOVABLE  
**Reason**: Entire section for Python 2.7 testing.

#### `.travis.yml:4` - Python 2.7 CI
```4:4:.travis.yml
  - "2.7"
```
**Status**: REMOVABLE  
**Reason**: Python 2.7 CI configuration.

---

## 4. Summary by File

### `docopt.py` (Core Library)
- **Python 2-specific**: `class Pattern(object):` (line 32) - harmless but can be simplified
- **Compatibility shims**: `hasattr(source, 'split')` check (line 285) - needs verification
- **Dead code**: Commented argument default parsing (lines 564-568), commented any_options code (lines 574-576)
- **Style**: Old-style % formatting (line 358)

### `test_docopt.py`
- **Python 2-specific**: `from __future__ import with_statement` (line 1), unicode string test (lines 444-449)
- **Dead code**: Multiple commented test functions and cases (lines 341-344, 364-365, 426-427, 467-481, 484-489, 510-529)
- **Style**: Old-style % formatting (multiple locations)

### `conftest.py`
- **Python 2-specific**: `simplejson` fallback (lines 2-5), old-style `super()` (line 51)
- **Compatibility shims**: `fspath` API usage (lines 38, 42, 76) - needs pytest API update
- **Style**: Old-style % formatting (lines 44, 70)

### `examples/config_file_example.py`
- **Python 2-specific**: ConfigParser/StringIO compatibility (lines 22-27), `readfp()` method (line 44)
- **Style**: dict() constructor style (lines 49, 60)

### Configuration Files
- **setup.py**: Python 2 classifiers (lines 36-37)
- **tox.ini**: Python 2.7 test environment (lines 7, 13-16)
- **.travis.yml**: Python 2.7 CI (line 4)

---

## 5. Recommended Action Plan

### Phase 1: Remove Python 2 Support Infrastructure
1. Remove Python 2 classifiers from `setup.py`
2. Remove Python 2.7 from `tox.ini` and `.travis.yml`
3. Update Python version requirements in documentation

### Phase 2: Remove Python 2 Compatibility Code
1. Remove `from __future__ import with_statement` from `test_docopt.py`
2. Simplify or remove `test_issue34_unicode_strings()` test
3. Remove `simplejson` fallback from `conftest.py`
4. Update `super()` calls to Python 3 style
5. Remove ConfigParser/StringIO compatibility from example files
6. Update `readfp()` to `read_file()` in example files

### Phase 3: Clean Up Dead Code
1. Remove all commented-out code blocks
2. Remove commented test functions
3. Address or remove FIXME comments

### Phase 4: Modernize APIs
1. Update pytest `fspath` API to `pathlib.Path`
2. Consider modernizing string formatting (optional, style only)

### Phase 5: Verify Behavior
1. Verify `hasattr(source, 'split')` check - determine if list support is intentional API
2. Run full test suite after changes
3. Update documentation if API changes

---

## Notes

- All changes should maintain backward compatibility for Python 3.10+ users
- Example files are less critical but should be updated for consistency
- Dead code removal is safe and improves maintainability
- Some style changes (% formatting) are optional but recommended for modern Python

