# Changelog

All notable changes to docopt will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-04

### Breaking Changes
- **Dropped Python 2.7 support** - Now requires Python 3.10 or higher
- **Dropped Python 3.4-3.9 support** - Minimum version is now Python 3.10

### Added
- Python 3.10, 3.11, 3.12, and 3.13 support
- Modern pathlib support throughout the codebase
- Type hints compatibility (preparation for future type annotations)

### Changed
- **Modernized codebase for Python 3.10+**
  - Removed all Python 2 compatibility code
  - Converted old-style classes to modern Python 3 classes
  - Replaced `%` string formatting with f-strings throughout
  - Updated to modern `super()` syntax without arguments
  - Migrated from deprecated pytest APIs to current versions
  
- **Updated dependencies and tooling**
  - Removed `simplejson` fallback (using standard library `json`)
  - Updated pytest integration to use `pathlib.Path` instead of `py.path.local`
  - Updated pytest hooks to use `from_parent()` factory methods
  - Modernized tox configuration for Python 3.10-3.13
  
- **Improved code quality**
  - Removed ~200 lines of dead/commented code
  - Cleaned up obsolete FIXME comments
  - Removed tests for removed features
  - Simplified unicode string handling (all strings are unicode in Python 3)

- **Updated package metadata**
  - Changed development status from "Alpha" to "Production/Stable"
  - Updated classifiers to reflect Python 3.10+ only
  - Added `python_requires='>=3.10'` to setup.py
  - Set wheel to non-universal (Python 3 only)
  - Added proper long_description_content_type

### Removed
- Python 2.7 support and all compatibility shims
- Python 3.4-3.9 support
- `from __future__` imports
- Obsolete `any_options` parameter tests
- Custom pytest test command class (no longer needed)
- ConfigParser/StringIO Python 2/3 compatibility code in examples
- Deprecated `config.readfp()` usage (replaced with `config.read_file()`)

### Fixed
- Updated deprecated pytest APIs to prevent warnings
- Modernized example files to use current best practices
- Fixed string formatting to use modern f-strings

### Internal
- Maintained exact type checking where needed (bool vs int distinction)
- Preserved all public API behavior - 100% backward compatible for Python 3.10+ users
- Improved code readability with modern Python idioms

### Migration Notes

**For users upgrading from 0.6.2:**

1. **Python Version**: Ensure you're running Python 3.10 or higher
   ```bash
   python --version  # Should be 3.10.0 or higher
   ```

2. **Installation**: No changes to import or usage
   ```python
   from docopt import docopt
   # All existing code continues to work unchanged
   ```

3. **No API Changes**: The public API remains 100% compatible. All existing code using docopt will continue to work without modifications.

4. **Testing**: If you were testing against Python 2.7 or 3.4-3.9, update your CI/CD to test against Python 3.10+

**For contributors:**

1. Development now requires Python 3.10+
2. Use `tox` to test against py310, py311, py312, py313
3. Code should use modern Python 3.10+ idioms (f-strings, pathlib, etc.)

---

## [0.6.2] - 2014-06-09

### Fixed
- Bugfix release

## [0.6.1] - 2014-06-09

### Fixed
- Fix issue #85 which caused improper handling of `[options]` shortcut if it was present several times

## [0.6.0] - 2013-02-07

### Added
- New argument `options_first`, disallows interspersing options and arguments
- If option with argument could be repeated, its default value will be interpreted as space-separated list

### Changed
- **Breaking**: Meaning of `[options]` shortcut slightly changed. Previously it meant *"any known option"*. Now it means *"any option not in usage-pattern"*
- **Breaking**: `argv` is `None` by default, not `sys.argv[1:]`. This allows `docopt` to always use the *latest* `sys.argv`

## [0.5.0] - 2012-10-03

### Added
- Repeated options/commands are counted or accumulated into a list

## [0.4.2] - 2012-08-28

### Fixed
- Bugfix release

## [0.4.0] - 2012-08-22

### Added
- Option descriptions become optional
- Support for "``--``" and "``-``" commands

## [0.3.0] - 2012-08-17

### Added
- Support for (sub)commands like `git remote add`
- Introduce `[options]` shortcut for any options

### Changed
- **Breaking**: `docopt` returns dictionary instead of namespace

## [0.2.0] - 2012-06-01

### Added
- Usage pattern matching
- Positional arguments parsing based on usage patterns

### Changed
- **Breaking**: `docopt` returns namespace (for arguments), not list
- **Breaking**: Usage pattern is formalized

## [0.1.0] - 2012-04-01

### Added
- Initial release
- Options-parsing only (based on options description)

---

## Version History Summary

- **1.0.0** (2025-01-04): Python 3.10+ modernization, production stable
- **0.6.2** (2014-06-09): Bugfix release
- **0.6.1** (2014-06-09): Fix `[options]` shortcut handling
- **0.6.0** (2013-02-07): Add `options_first` parameter
- **0.5.0** (2012-10-03): Repeated options/commands support
- **0.4.2** (2012-08-28): Bugfix release
- **0.4.0** (2012-08-22): Optional option descriptions
- **0.3.0** (2012-08-17): Subcommands and `[options]` shortcut
- **0.2.0** (2012-06-01): Usage pattern matching
- **0.1.0** (2012-04-01): Initial release

[1.0.0]: https://github.com/docopt/docopt/compare/0.6.2...1.0.0
[0.6.2]: https://github.com/docopt/docopt/compare/0.6.1...0.6.2
[0.6.1]: https://github.com/docopt/docopt/compare/0.6.0...0.6.1
[0.6.0]: https://github.com/docopt/docopt/compare/0.5.0...0.6.0
[0.5.0]: https://github.com/docopt/docopt/compare/0.4.2...0.5.0
[0.4.2]: https://github.com/docopt/docopt/compare/0.4.0...0.4.2
[0.4.0]: https://github.com/docopt/docopt/compare/0.3.0...0.4.0
[0.3.0]: https://github.com/docopt/docopt/compare/0.2.0...0.3.0
[0.2.0]: https://github.com/docopt/docopt/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/docopt/docopt/releases/tag/0.1.0

