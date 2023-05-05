%{!?python3_inc:%global python3_inc %(%{__python3} -c "from distutils.sysconfig import get_python_inc; print(get_python_inc(1))")}
%global PYINCLUDE %{_includedir}/python%{python3_version}
%global rpm_macros_dir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)
%undefine _strict_symbol_defs_build
%global wx_siplib 1
%global pyqt5_sip 1

Summary: SIP - Python/C++ Bindings Generator
Name: 	 sip
Version: 4.19.25
Release: 2
License: GPLv2 or GPLv3
Url: https://riverbankcomputing.com/software/sip/intro
Source0: https://riverbankcomputing.com/static/Downloads/sip/%{version}/sip-%{version}.tar.gz
Source1: macros.sip
Source10: sip-wrapper.sh

Patch50: sip-4.18-no_strip.patch
Patch51: sip-4.18-no_rpath.patch
Patch53: sip-4.19.18-no_hardcode_sip_so.patch
Patch54: sip-4.19.25-py_ssize_t_clean.patch
Patch55: support-specify-cc.patch

BuildRequires: make
BuildRequires: gcc-c++
BuildRequires: sed
BuildRequires: bison
BuildRequires: flex

Obsoletes: sip-macros < %{version}-%{release}
Provides:  sip-macros = %{version}-%{release}

%global _description\
SIP is a tool for generating bindings for C++ classes so that they can be\
accessed as normal Python classes. SIP takes many of its ideas from SWIG but,\
because it is specifically designed for C++ and Python, is able to generate\
tighter bindings. SIP is so called because it is a small SWIG.\
\
SIP was originally designed to generate Python bindings for KDE and so has\
explicit support for the signal slot mechanism used by the Qt/KDE class\
libraries. However, SIP can be used to generate Python bindings for any C++\
class library.

%description %_description

%package doc
Summary: Documentation for %summary
BuildArch: noarch
%description doc
This package contains HTML documentation for SIP.
%_description


%package -n python3-sip
Summary: SIP - Python 3/C++ Bindings Generator
Provides: python3-sip-api(12) = 12.7
%description -n python3-sip
This is the Python 3 build of SIP.

%_description

%package -n python3-sip-devel
Summary: Files needed to generate Python bindings for any C++ class library
Requires: sip = %{version}-%{release}
BuildRequires: python3-devel
Requires:      python3-devel
%description -n python3-sip-devel
%{summary}.

%package -n python3-pyqt4-sip
Summary: SIP - Python 3/C++ Bindings Generator for pyqt4
BuildRequires: python3-devel
Provides: python3-pyqt4-sip-api(12) = 12.7
%description -n python3-pyqt4-sip
This is the Python 3 build of pyqt4-SIP.

%package -n python3-pyqt5-sip
Summary: SIP - Python 3/C++ Bindings Generator for pyqt5
BuildRequires: python3-devel
Provides: python3-pyqt5-sip-api(12) = 12.7
%description -n python3-pyqt5-sip
This is the Python 3 build of pyqt5-SIP.

%package -n python3-wx-siplib
Summary: SIP - Python 3/C++ Bindings Generator for wx
BuildRequires: python3-devel
Provides: python3-wx-siplib-api(12) = 12.7
Provides: python3-wx-siplib-api(12) = 12.7
%description -n python3-wx-siplib
This is the Python 3 build of wx-siplib.

%_description



%prep

%setup -q -n %{name}-%{version}

%patch50 -p1 -b .no_strip
%patch51 -p1 -b .no_rpath
%patch53 -p1 -b .no_sip_so
%patch54 -p1 -b .py_ssize_t_clean
%patch55 -p1


%build
flex --outfile=sipgen/lexer.c sipgen/metasrc/lexer.l
bison --yacc --defines=sipgen/parser.h --output=sipgen/parser.c sipgen/metasrc/parser.y
sed -i -e 's|target = siplib|target = sip|g' siplib/siplib.sbf

mkdir %{_target_platform}-python3
pushd %{_target_platform}-python3
%if "%toolchain" == "clang"
  %{__python3} ../configure.py -p linux-clang \
  -b %{_bindir} -d %{python3_sitearch} -e %{PYINCLUDE} \
  CXXFLAGS+="%{optflags}" CFLAGS+="%{optflags}" LFLAGS+="%{?__global_ldflags}"
%else
%{__python3} ../configure.py \
  -b %{_bindir} -d %{python3_sitearch} -e %{PYINCLUDE} \
  CXXFLAGS+="%{optflags}" CFLAGS+="%{optflags}" LFLAGS+="%{?__global_ldflags}"
%endif

%make_build
popd

mkdir %{_target_platform}-python3-pyqt4
pushd %{_target_platform}-python3-pyqt4
%if "%toolchain" == "clang"
%{__python3} ../configure.py -p linux-clang \
  --sip-module=PyQt4.sip \
  -b %{_bindir} -d %{python3_sitearch} -e %{PYINCLUDE} \
  CXXFLAGS+="%{optflags}" CFLAGS+="%{optflags}" LFLAGS+="%{?__global_ldflags}"
%else
%{__python3} ../configure.py \
  --sip-module=PyQt4.sip \
  -b %{_bindir} -d %{python3_sitearch} -e %{PYINCLUDE} \
  CXXFLAGS+="%{optflags}" CFLAGS+="%{optflags}" LFLAGS+="%{?__global_ldflags}"
%endif

%make_build
popd

mkdir %{_target_platform}-python3-pyqt5
pushd %{_target_platform}-python3-pyqt5
%if "%toolchain" == "clang"
%{__python3} ../configure.py -p linux-clang \
  --sip-module=PyQt5.sip \
  -b %{_bindir} -d %{python3_sitearch} -e %{PYINCLUDE} \
  CXXFLAGS+="%{optflags}" CFLAGS+="%{optflags}" LFLAGS+="%{?__global_ldflags}"
%else
%{__python3} ../configure.py \
  --sip-module=PyQt5.sip \
  -b %{_bindir} -d %{python3_sitearch} -e %{PYINCLUDE} \
  CXXFLAGS+="%{optflags}" CFLAGS+="%{optflags}" LFLAGS+="%{?__global_ldflags}"
%endif

%make_build
popd

sed -i -e 's|target = sip|target = siplib|g' siplib/siplib.sbf
mkdir %{_target_platform}-python3-wx
pushd %{_target_platform}-python3-wx
%if "%toolchain" == "clang"
%{__python3} ../configure.py -p linux-clang \
  --sip-module=wx.siplib \
  -b %{_bindir} -d %{python3_sitearch} -e %{PYINCLUDE} \
  CXXFLAGS+="%{optflags}" CFLAGS+="%{optflags}" LFLAGS+="%{?__global_ldflags}"
%else
%{__python3} ../configure.py \
  --sip-module=wx.siplib \
  -b %{_bindir} -d %{python3_sitearch} -e %{PYINCLUDE} \
  CXXFLAGS+="%{optflags}" CFLAGS+="%{optflags}" LFLAGS+="%{?__global_ldflags}"
%endif


%make_build
popd
sed -i -e 's|target = siplib|target = sip|g' siplib/siplib.sbf


%install
%make_install -C %{_target_platform}-python3
%make_install -C %{_target_platform}-python3-pyqt4
%make_install -C %{_target_platform}-python3-pyqt5
%make_install -C %{_target_platform}-python3-wx
mv %{buildroot}%{python3_sitearch}/wx/sip.pyi %{buildroot}%{python3_sitearch}/wx/siplib.pyi
ln -s sip %{buildroot}%{_bindir}/python3-sip
mkdir -p %{buildroot}%{python3_sitearch}/__pycache__/exclude_rpm_hack

install %{SOURCE10} %{buildroot}%{_bindir}/sip-pyqt4
install %{SOURCE10} %{buildroot}%{_bindir}/sip-pyqt5
install %{SOURCE10} %{buildroot}%{_bindir}/sip-wx
sed -i -e 's|@SIP_MODULE@|PyQt4.sip|g' %{buildroot}%{_bindir}/sip-pyqt4
sed -i -e 's|@SIP_MODULE@|PyQt5.sip|g' %{buildroot}%{_bindir}/sip-pyqt5
sed -i -e 's|@SIP_MODULE@|wx.siplib|g' %{buildroot}%{_bindir}/sip-wx

mkdir -p %{buildroot}%{_datadir}/sip
install -D -p -m644 %{SOURCE1} %{buildroot}%{rpm_macros_dir}/macros.sip
pushd doc
find html/ -type f -exec install -m0644 -D {} %{buildroot}%{_pkgdocdir}/{} \;
popd


%files
%doc README LICENSE LICENSE-GPL2 LICENSE-GPL3
%{_bindir}/sip
# sip-wrappers
%{_bindir}/sip-pyqt4
%{_bindir}/sip-pyqt5
%{_bindir}/sip-wx
# compat symlink
%{_bindir}/python3-sip
%dir %{_datadir}/sip/
%{rpm_macros_dir}/macros.sip

%files doc
%{_pkgdocdir}/html

%files -n python3-sip-devel
%{PYINCLUDE}/sip.h
%{python3_sitearch}/sipconfig.py*
%{python3_sitearch}/sipdistutils.py*
%{python3_sitearch}/__pycache__/*
%exclude %{python3_sitearch}/__pycache__/exclude_rpm_hack

%files -n python3-sip
%doc NEWS README LICENSE LICENSE-GPL2 LICENSE-GPL3
%{python3_sitearch}/sip.*
%{python3_sitearch}/sip-%{version}.dist-info/

%files -n python3-pyqt4-sip
%doc NEWS README LICENSE LICENSE-GPL2 LICENSE-GPL3
%dir %{python3_sitearch}/PyQt4/
%{python3_sitearch}/PyQt4/sip.*
%{python3_sitearch}/PyQt4_sip-%{version}.dist-info/

%files -n python3-pyqt5-sip
%doc NEWS README LICENSE LICENSE-GPL2 LICENSE-GPL3
%dir %{python3_sitearch}/PyQt5/
%{python3_sitearch}/PyQt5/sip.*
%{python3_sitearch}/PyQt5_sip-%{version}.dist-info/

%files -n python3-wx-siplib
%doc NEWS README LICENSE LICENSE-GPL2 LICENSE-GPL3
%dir %{python3_sitearch}/wx/
%{python3_sitearch}/wx/siplib.*
%{python3_sitearch}/wx_siplib-%{version}.dist-info/

%changelog
* Mon Apr 17 2023 jammyjellyfish <jammyjellyfish255@outlook.com> - 4.19.25-2
- Support specify CC

* Sat Jan 29 2022 chenchen <chen_aka_jan@163.com> - 4.19.25-1
- update to 4.19.25

* Tue Jan 05 2021 maminjie <maminjie1@huawei.com> - 4.19.12-12
- resolve installation conflicts of sub-packages
- fix license

* Wed Oct 21 2020 wutao <wutao61@huawei.com> - 4.19.12-11
- delete python2 modules

* Thu Nov 28 2019 Ling Yang <lingyang2@huawei.com> - 4.19.12-10
- Package init
