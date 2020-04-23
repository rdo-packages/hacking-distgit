%global pypi_name hacking

# disable tests for now, see
# https://bugs.launchpad.net/hacking/+bug/1652409
# https://bugs.launchpad.net/hacking/+bug/1607942
# https://bugs.launchpad.net/hacking/+bug/1652411
%global with_tests 0

%global with_doc 1

%global common_desc OpenStack Hacking Guideline Enforcement

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-%{pypi_name}
Version:        3.0.0
Release:        1%{?dist}
Summary:        OpenStack Hacking Guideline Enforcement

License:        ASL 2.0
URL:            http://github.com/openstack-dev/hacking
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
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

%package -n python3-%{pypi_name}
Summary:        OpenStack Hacking Guideline Enforcement
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  git
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
BuildRequires:  python3-subunit
BuildRequires:  python3-testrepository
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools
BuildRequires:  python3-six
BuildRequires:  python3-mock
BuildRequires:  python3-flake8 >= 2.6.0
%if 0%{?with_doc}
BuildRequires:  python3-sphinx
BuildRequires:  python3-openstackdocstheme
%endif
BuildRequires:  python3-pyflakes
BuildRequires:  python3-mccabe

Requires: python3-pbr
Requires: python3-flake8 >= 3.6.0
Requires: python3-six
Requires: python3-pyflakes

%description -n python3-%{pypi_name}
%{common_desc}
%if 0%{?fedora}
**NOTE**: the local-check feature is DISABLED in this package! See
https://bugs.launchpad.net/hacking/+bug/1652409 for details.
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
%{py3_build}

%if 0%{?with_doc}
# generate html docs
sphinx-build-3 -W -b html doc/source doc/build/html
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

%check
%if 0%{?with_tests}
%{__python3} setup.py test
%endif

%files -n python3-%{pypi_name}
%if 0%{?with_doc}
%doc doc/build/html README.rst
%else
%doc README.rst
%endif
%license LICENSE
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/%{pypi_name}

%changelog
* Thu Apr 23 2020 RDO <dev@lists.rdoproject.org> 3.0.0-1
- Update to 3.0.0

