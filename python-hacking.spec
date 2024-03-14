%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2ef3fe0ec2b075ab7458b5f8b702b20b13df2318
%global pypi_name hacking

# disable tests for now, see
# https://bugs.launchpad.net/hacking/+bug/1652409
# https://bugs.launchpad.net/hacking/+bug/1607942
# https://bugs.launchpad.net/hacking/+bug/1652411
%global with_tests 0

%global with_doc 1

%global common_desc OpenStack Hacking Guideline Enforcement

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order

Name:           python-%{pypi_name}
Version:        6.1.0
Release:        1%{?dist}
Summary:        OpenStack Hacking Guideline Enforcement

License:        Apache-2.0
URL:            http://github.com/openstack-dev/hacking
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
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

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

%description
%{common_desc}
%if 0%{?fedora}
**NOTE**: the local-check feature is DISABLED in this package! See
https://bugs.launchpad.net/hacking/+bug/1652409 for details.
%endif

%package -n python3-%{pypi_name}
Summary:        OpenStack Hacking Guideline Enforcement

BuildRequires:  git-core
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

%description -n python3-%{pypi_name}
%{common_desc}
%if 0%{?fedora}
**NOTE**: the local-check feature is DISABLED in this package! See
https://bugs.launchpad.net/hacking/+bug/1652409 for details.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# remove /usr/bin/env from core.py
sed -i '1d' hacking/core.py

# remove /usr/bin/env from tests/test_doctest.py
sed -i '1d' hacking/tests/test_doctest.py


sed -i /.*-c{env:TOX_CONSTRAINTS_FILE.*/d tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs};do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%if 0%{?with_doc}
# generate html docs
%tox -e docs
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo} doc/build/html/objects.inv
%endif

%install
%pyproject_install

%check
%if 0%{?with_tests}
%tox -e %{default_toxenv}
%endif

%files -n python3-%{pypi_name}
%if 0%{?with_doc}
%doc doc/build/html README.rst
%else
%doc README.rst
%endif
%license LICENSE
%{python3_sitelib}/*.dist-info
%{python3_sitelib}/%{pypi_name}

%changelog
* Thu Mar 14 2024 RDO <dev@lists.rdoproject.org> 6.1.0-1
- Update to 6.1.0

