%global pypi_name hacking

%if 0%{?fedora}
%global with_python3 1
%endif

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-%{pypi_name}
Version:        0.10.2
Release:        3%{?dist}
Summary:        OpenStack Hacking Guideline Enforcement

License:        ASL 2.0
URL:            http://github.com/openstack-dev/hacking
Source0:        https://pypi.python.org/packages/source/h/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
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

Requires: python3-pbr
Requires: python3-pyflakes
Requires: python3-flake8
Requires: python3-six

%description  -n python3-%{pypi_name}
OpenStack Hacking Guidline Enforcement
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
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Sep 01 2015 Lukas Bezdicka <lbezdick@redhat.com> - 0.10.2-1
- Add python3 sub package and update to 0.10.2

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 03 2015 Matthias Runge <mrunge@redhat.com> - 0.10.1-1
- update to 0.10.1

* Mon Oct 20 2014 Matthias Runge <mrunge@redhat.com> - 0.9.2-1
- udapte to 0.9.2

* Tue Jun 10 2014 Matthias Runge <mrunge@redhat.com> - 0.9.1-1
- update to 0.9.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

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
