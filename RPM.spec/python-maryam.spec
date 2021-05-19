# Created by pyp2rpm-3.3.6
%global pypi_name maryam

Name:           python-%{pypi_name}
Version:        2.2.6.post1
Release:        1%{?dist}
Summary:        OWASP Maryam is a modular/optional open source framework based on OSINT and data gathering

License:        GPL-V3
URL:            https://github.com/saeeddhqan/Maryam
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

%description
[![Build Status]( ![Version 2.2.6]( ![GPLv3 License]( ![Python 3.8.x](
[![Codacy Badge]( [![CII Best Practices](

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:       python3dist(bs4)
Requires:       python3dist(cloudscraper)
Requires:       python3dist(flask)
Requires:       python3dist(lxml)
Requires:       python3dist(requests)
%description -n python3-%{pypi_name}
[![Build Status]( ![Version 2.2.6]( ![GPLv3 License]( ![Python 3.8.x](
[![Codacy Badge]( [![CII Best Practices](


%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.md
%{_bindir}/maryam
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info

%changelog
* Tue May 18 2021 John Doe <john@doe.com> - 2.2.6.post1-1
- Initial package.