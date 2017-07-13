%global pypi_name hacking

%if 0%{?fedora} > 21
%global with_python3 1
%endif

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        OpenStack Hacking Guideline Enforcement

License:        ASL 2.0
URL:            http://github.com/openstack-dev/hacking
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%description
OpenStack Hacking Guideline Enforcement

%package -n python2-%{pypi_name}
Summary:        OpenStack Hacking Guideline Enforcement
%{?python_provide:%python_provide python2-%{pypi_name}}

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
BuildRequires:  python-mock

Requires: python-pbr
Requires: pyflakes
Requires: python-flake8
Requires: python-six

%description -n python2-%{pypi_name}
OpenStack Hacking Guideline Enforcement

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        OpenStack Hacking Guideline Enforcement
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-d2to1
BuildRequires:  python3-pbr
BuildRequires:  python3-sphinx
BuildRequires:  python3-flake8
BuildRequires:  python3-subunit
BuildRequires:  python3-sphinx
BuildRequires:  python3-testrepository
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools
BuildRequires:  python3-oslo-sphinx
BuildRequires:  python3-pep8
BuildRequires:  python3-six
BuildRequires:  python3-flake8
BuildRequires:  python3-pyflakes
BuildRequires:  python3-mccabe
BuildRequires:  python3-mock

Requires: python3-pbr
Requires: python3-pyflakes
Requires: python3-flake8
Requires: python3-six

%description  -n python3-%{pypi_name}
OpenStack Hacking Guideline Enforcement
%endif

%prep
%setup -q -n %{pypi_name}-%{upstream_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# remove /usr/bin/env from core.py
sed -i '1d' hacking/core.py

# remove /usr/bin/env from tests/test_doctest.py
sed -i '1d' hacking/tests/test_doctest.py

rm -rf {test-,}requirements.txt

%build
%{__python2} setup.py build

# generate html docs 
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%if 0%{?with_python3}
%{__python3} setup.py build
# generate html docs 
#sphinx-build doc/source html
# remove the sphinx-build leftovers
#rm -rf html/.{doctrees,buildinfo}
%endif

%install
%{__python2} setup.py install --skip-build --root %{buildroot}
%if 0%{?with_python3}
%{__python3} setup.py install --skip-build --root %{buildroot}
%endif

%check
%{__python2} setup.py test
%if 0%{?with_python3}
# "Expecting a string b" error from test library
#rm -rf .testrepository/
#%{__python3} setup.py test
%endif

%files -n python2-%{pypi_name}
%doc html README.rst
%license LICENSE
%{python2_sitelib}/*.egg-info
%{python2_sitelib}/%{pypi_name}

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc html README.rst
%license LICENSE
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/%{pypi_name}
%endif

%changelog

# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack-dev/hacking/commit/?id=5fa587dfedbf93535d19fb61e41ca117373a719c
