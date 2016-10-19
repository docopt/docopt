#
# spec file for package python-docopt
#
# Copyright (c) 2016 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           python-docopt
Version:        0.6.2
Release:        1
Url:            https://github.com/docopt/docopt
Summary:        Pythonic command line arguments parser, that will make you smile 
License:        MIT
Group:          Development/Languages/Python
Source:         https://github.com/docopt/docopt/archive/%{version}.tar.gz
BuildRequires:  python-setuptools
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
docopt helps you to define the interface for your command-line app, and
automatically generate a parser for it.

docopt is based on conventions that have been used for decades in 
help messages and man pages for describing a program's interface.
An interface description in docopt is such a help message, 
but formalized.

This is the python implementation of docopt.

%prep
%setup -q -n docopt-%{version}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE-MIT README.rst
%{python_sitelib}

%changelog
* Tue Oct 19 2016 Benoit Mortier <benoit.mortier@opensides.be> - 0.6.2-1
- First release




