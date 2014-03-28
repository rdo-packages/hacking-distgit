%global pypi_name hacking

Name:           python-%{pypi_name}
Version:        0.8.1
Release:        1%{?dist}
Summary:        OpenStack Hacking Guideline Enforcement

License:        ASL 2.0
URL:            http://github.com/openstack-dev/hacking
Source0:        http://pypi.python.org/packages/source/h/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-d2to1
BuildRequires:  python-pbr
BuildRequires:  python-sphinx
BuildRequires:  python-flake8
BuildRequires:  python-subunit
BuildRequires:  python-sphinx
BuildRequires:  python-testrepository
BuildRequires:  python-testscenarios
BuildRequires:  python-testtools
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-pep8
BuildRequires:  python-six
BuildRequires:  python-flake8
BuildRequires:  pyflakes
BuildRequires:  python-mccabe

Requires: python-pbr
Requires: pyflakes
Requires: python-flake8
Requires: python-six


%description
OpenStack Hacking Guidline Enforcement


%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# remove /usr/bin/env from core.py
sed -i '1d' hacking/core.py

# remove /usr/bin/env from tests/test_doctest.py
sed -i '1d' hacking/tests/test_doctest.py

#remove discover from test-requirements as it's in py27
sed -i '/discover/d' test-requirements.txt
# strip off version numbers from test equirements as they're handled in rpm
sed -i 's/>.*$//' test-requirements.txt
rm requirements.txt
rm test-requirements.txt

# python-oslo-sphinx was upstream renamed to python-oslosphinx. We still
# use the former version.
sed -i 's|oslosphinx|oslo.sphinx|' doc/source/conf.py

%build
%{__python} setup.py build

# generate html docs 
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%{__python} setup.py install --skip-build --root %{buildroot}

%check
%{__python} setup.py test

%files
%doc html README.rst LICENSE
%{python_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%{python_sitelib}/%{pypi_name}

%changelog
* Fri Mar 28 2014 Matthias Runge <mrunge@redhat.com> - 0.8.1-1
- update to 0.8.1

* Tue Nov 19 2013 Matthias Runge <mrunge@redhat.com> - 0.8.0-1
- update to 0.8.0

* Tue Sep 17 2013 Matthias Runge <mrunge@redhat.com> - 0.7.2-1
- update to 0.7.2

* Fri Jun 07 2013 Matthias Runge <mrunge@redhat.com> - 0.5.3-2
- also use checks and move requirements to rpm-requiremens

* Mon Apr 29 2013 Matthias Runge <mrunge@redhat.com> - 0.5.3-1
- Initial package.
