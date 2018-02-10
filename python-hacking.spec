%global pypi_name hacking

%global commit 865398f0c9a20883ef1ab68a9f80ffd74b9098e8
%global shortcommit %(c=%{commit}; echo ${c:0:7})
# DO NOT REMOVE ALPHATAG
%global alphatag .%{shortcommit}git

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

%{!?upstream_version: %global upstream_version %{shortcommit}}

Name:           python-%{pypi_name}
Version:        1.0.0
Release:        1%{?alphatag}%{?dist}
Summary:        OpenStack Hacking Guideline Enforcement

License:        ASL 2.0
URL:            http://github.com/openstack-dev/hacking
Source0:        https://github.com/openstack-dev/%{pypi_name}/archive/%{commit}.tar.gz#/%{pypi_name}-%{shortcommit}.tar.gz
#Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
%if 0%{?fedora}
# FIXME(apevec) patches do not apply after https://review.openstack.org/514934
# Mostly adapt tests to work with both flake8 2.x and 3.x. Note,
# local-checks feature is entirely broken with 3.x. Will send upstream
# when I find a way to do it which doesn't involve signing my
# firstborn over to the openstack foundation
#Patch0:         0001-Tests-adapt-to-flake8-3.x.patch
# Hack out the 'local-checks' feature, since it doesn't work anyway,
# to avoid the dep it introduces on pep8, and disable the test for the
# feature. Only apply on releases with flake8 3.x.
#Patch1:         0002-Disable-local-checks.patch
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
BuildRequires:  python2-setuptools
BuildRequires:  python2-pbr
BuildRequires:  python2-sphinx
BuildRequires:  python2-subunit
BuildRequires:  python2-testrepository
BuildRequires:  python2-testscenarios
BuildRequires:  python2-testtools
BuildRequires:  python2-openstackdocstheme
BuildRequires:  python2-six
BuildRequires:  python2-mock
BuildRequires:  python2-flake8 >= 2.6.0
%if 0%{?fedora} || 0%{?rhel} > 7
BuildRequires:  python2-pyflakes
BuildRequires:  python2-d2to1
BuildRequires:  python2-mccabe
%else
BuildRequires:  pyflakes
BuildRequires:  python-d2to1
BuildRequires:  python-mccabe
%endif

Requires: python2-pbr
Requires: python2-flake8 >= 2.6.0
Requires: python2-six
%if 0%{?fedora} || 0%{?rhel} > 7
Requires: python2-pyflakes
%else
Requires: pyflakes
%endif

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
BuildRequires:  python3-flake8 >= 2.6.0
BuildRequires:  python3-subunit
BuildRequires:  python3-testrepository
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools
BuildRequires:  python3-six
BuildRequires:  python3-pyflakes
BuildRequires:  python3-mccabe
BuildRequires:  python3-mock

Requires: python3-pbr
Requires: python3-pyflakes
Requires: python3-flake8 >= 2.6.0
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

rm -rf {test-,}requirements.txt

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
* Sat Feb 10 2018 RDO <dev@lists.rdoproject.org> 1.0.0-1
- Update to 1.0.0
- Use commit 865398f0 to include pep8 to pycodestyle transition path


