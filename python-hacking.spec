%global pypi_name hacking

%if 0%{?fedora}
%global with_python3 1
# disable tests for now, see
# https://bugs.launchpad.net/hacking/+bug/1652409
# https://bugs.launchpad.net/hacking/+bug/1607942
# https://bugs.launchpad.net/hacking/+bug/1652411
%global with_tests 0
%else
%global with_tests 1
%endif

%global common_desc OpenStack Hacking Guideline Enforcement

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        OpenStack Hacking Guideline Enforcement

License:        ASL 2.0
URL:            http://github.com/openstack-dev/hacking
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
%if 0%{?fedora}
# Mostly adapt tests to work with both flake8 2.x and 3.x. Note,
# local-checks feature is entirely broken with 3.x. Will send upstream
# when I find a way to do it which doesn't involve signing my
# firstborn over to the openstack foundation
Patch0:         0001-Tests-adapt-to-flake8-3.x.patch
# Hack out the 'local-checks' feature, since it doesn't work anyway,
# to avoid the dep it introduces on pep8, and disable the test for the
# feature. Only apply on releases with flake8 3.x.
Patch1:         0002-Disable-local-checks.patch
%endif
BuildArch:      noarch

%description
%{common_desc}
%if 0%{?fedora}
**NOTE**: the local-check feature is DISABLED in this package! See
https://bugs.launchpad.net/hacking/+bug/1652409 for details.
%endif

%package -n python2-%{pypi_name}
Summary:        OpenStack Hacking Guideline Enforcement
%{?python_provide:%python_provide python2-%{pypi_name}}

BuildRequires:  git
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-d2to1
BuildRequires:  python-pbr
BuildRequires:  python-sphinx
BuildRequires:  python-flake8
BuildRequires:  python-subunit
BuildRequires:  python-testrepository
BuildRequires:  python-testscenarios
BuildRequires:  python-testtools
BuildRequires:  python-openstackdocstheme
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
%{common_desc}
%if 0%{?fedora}
**NOTE**: the local-check feature is DISABLED in this package! See
https://bugs.launchpad.net/hacking/+bug/1652409 for details.
%endif

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        OpenStack Hacking Guideline Enforcement
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-d2to1
BuildRequires:  python3-pbr
BuildRequires:  python3-flake8
BuildRequires:  python3-subunit
BuildRequires:  python3-testrepository
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools
BuildRequires:  python3-pep8
BuildRequires:  python3-six
BuildRequires:  python3-flake8
BuildRequires:  python3-pyflakes
BuildRequires:  python3-mccabe
BuildRequires:  python3-mock
BuildRequires:  openstack-macros

Requires: python3-pbr
Requires: python3-pyflakes
Requires: python3-flake8
Requires: python3-six

%description  -n python3-%{pypi_name}
%{common_desc}
%if 0%{?fedora}
**NOTE**: the local-check feature is DISABLED in this package! See
https://bugs.launchpad.net/hacking/+bug/1652409 for details.
%endif
%endif

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# remove /usr/bin/env from core.py
sed -i '1d' hacking/core.py

# remove /usr/bin/env from tests/test_doctest.py
sed -i '1d' hacking/tests/test_doctest.py

%py_req_cleanup

%build
%{__python2} setup.py build

# generate html docs 
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

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
%if 0%{?with_tests}
%{__python2} setup.py test
%if 0%{?with_python3}
rm -rf .testrepository/
%{__python3} setup.py test
%endif
%endif

%files -n python2-%{pypi_name}
%doc doc/build/html README.rst
%license LICENSE
%{python2_sitelib}/*.egg-info
%{python2_sitelib}/%{pypi_name}

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc doc/build/html README.rst
%license LICENSE
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/%{pypi_name}
%endif

%changelog

