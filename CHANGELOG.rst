=========
Changelog
=========

**docopt** follows `semantic versioning <http://semver.org>`_.  The
first release with stable API will be 1.0.0 (soon).  Until then, you
are encouraged to specify explicitly the version in your dependency
tools, e.g.::

    pip install docopt==0.6.1



0.6.2
=====

- Added Wheel support



0.6.1
=====

- Fix issue `#85 <https://github.com/docopt/docopt/issues/85>`_
  which caused improper handling of ``[options]`` shortcut
  if it was present several times.



0.6.0
=====

- New argument ``options_first``, disallows interspersing options
  and arguments.  If you supply ``options_first=True`` to
  ``docopt``, it will interpret all arguments as positional
  arguments after first positional argument.

- If option with argument could be repeated, its default value
  will be interpreted as space-separated list. E.g. with
  ``[default: ./here ./there]`` will be interpreted as
  ``['./here', './there']``.

Breaking changes:

- Meaning of ``[options]`` shortcut slightly changed. Previously
  it meant *"any known option"*. Now it means *"any option not in
  usage-pattern"*.  This avoids the situation when an option is
  allowed to be repeated unintentionally.

- ``argv`` is ``None`` by default, not ``sys.argv[1:]``.
  This allows ``docopt`` to always use the *latest* ``sys.argv``,
  not ``sys.argv`` during import time.



0.5.0
=====

Repeated options/commands are counted or accumulated into a list.



0.4.2
=====

Bugfix release.



0.4.0
=====

Option descriptions become optional, 
support for "``--``" and "``-``" commands.



0.3.0
=====

Support for (sub)commands like `git remote add`.
Introduce ``[options]`` shortcut for any options.
**Breaking changes**: ``docopt`` returns dictionary.



0.2.0
=====

Usage pattern matching. Positional arguments parsing based on
usage patterns.
**Breaking changes**: ``docopt`` returns namespace (for arguments),
not list. Usage pattern is formalized.



0.1.0
=====

Initial release. Options-parsing only (based on options
description).
