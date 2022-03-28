#
# Conditional build:
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	prctl
Summary:	Allows to control specific characteristics of a process’ behaviour
Name:		python-%{module}
Version:	1.5.0
Release:	2
License:	GPL v3
Group:		Libraries/Python
Source0:	https://github.com/seveas/python-prctl/archive/v%{version}.tar.gz
# Source0-md5:	1fb338e9ffce5f654c91e8d44b018734
URL:		https://pythonhosted.org/python-prctl/
BuildRequires:	python-devel
BuildRequires:	python-distribute
BuildRequires:	rpm-pythonprov
# if py_postclean is used
BuildRequires:	rpmbuild(macros) >= 1.710
# when python3 present
BuildRequires:	libcap-devel
BuildRequires:	sed >= 4.0
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-modules
%endif
Requires:	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The linux prctl function allows you to control specific
characteristics of a process’ behaviour.

%package -n python3-%{module}
Summary:	Allows to control specific characteristics of a process’ behaviour
Group:		Libraries/Python

%description -n python3-%{module}
The linux prctl function allows you to control specific
characteristics of a process’ behaviour.

%package apidoc
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidoc
API documentation for %{module}.

%description apidoc -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q

%build
%if %{with python2}
%py_build
%endif

%if %{with python3}
%py3_build
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README
%{py_sitedir}/*.py[co]
%attr(755,root,root) %{py_sitedir}/*.so
%if "%{py_ver}" > "2.4"
%{py_sitedir}/python_%{module}-*.egg-info
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README
%{py3_sitedir}/__pycache__/%{module}.*.py[co]
%{py3_sitedir}/%{module}.py
%attr(755,root,root) %{py3_sitedir}/_%{module}.*.so
%{py3_sitedir}/python_%{module}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidoc
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
