%{!?python2_inc:%global python2_inc %(%{__python2} -c "from distutils.sysconfig import get_python_inc; print get_python_inc(1)")}
%{!?python3_inc:%global python3_inc %(%{__python3} -c "from distutils.sysconfig import get_python_inc; print(get_python_inc(1))")}
%{!?python2_sitearch:%global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

%global rpm_macros_dir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

%undefine _strict_symbol_defs_build

Name:           sip
Version:        4.19.12
Release:        12
Summary:        A C/C++ library bindings generator for Python v2 and v3
# sipgen/parser.{c.h} is GPLv2 with exceptions (bison)
License:        GPLv2 and (GPLv2 with exceptions) or GPLv3
URL:            http://www.riverbankcomputing.com/software/sip/intro
Source0:        http://downloads.sourceforge.net/pyqt/sip-%{version}.tar.gz
Source1:        macros.sip
Source2:        sip-wrapper.sh
BuildRequires:  gcc-c++ sed
Obsoletes:      sip-macros < %{version}-%{release}
Provides:       sip-macros = %{version}-%{release}
Patch0001:      sip-4.18-no_strip.patch
Patch0002:      sip-4.18-no_rpath.patch

%description
SIP is a tool that makes it very easy to create Python bindings for C and C++
libraries. It was originally developed to create PyQt, the Python bindings for
the Qt toolkit, but can be used to create bindings for any C or C++ library.

SIP comprises a code generator and a Python module. The code generator processes
a set of specification files and generates C or C++ code which is then compiled
to create the bindings extension module. The SIP Python module provides support
functions to the automatically generated code.

%package -n     python3-sip
Summary:        A C/C++ library bindings generator for Python v3
Provides:       python3-sip-api(12) = 12.5 python3-sip-api(12) = 12.5

%description -n python3-sip
This is the Python 3 build of SIP.

SIP is a tool that makes it very easy to create Python bindings for C and C++
libraries. It was originally developed to create PyQt, the Python bindings for
the Qt toolkit, but can be used to create bindings for any C or C++ library.

SIP comprises a code generator and a Python module. The code generator processes
a set of specification files and generates C or C++ code which is then compiled
to create the bindings extension module. The SIP Python module provides support
functions to the automatically generated code.

%package -n     python3-sip-devel
Summary:        Files needed to generate Python v3 bindings for any C++ class library
Requires:       sip = %{version}-%{release} python3-devel
BuildRequires:  python3-devel

%description -n python3-sip-devel
Files needed to generate Python v3 bindings for any C++ class library

%package -n     python3-pyqt4-sip
Summary:        Python 3/C++ Bindings Generator for pyqt4
Provides:       python3-pyqt4-sip-api(12) = 12.5 python3-pyqt4-sip-api(12) = 12.5
BuildRequires:  python3-devel

%description -n python3-pyqt4-sip
This is the Python 3 build of pyqt4-SIP.

SIP is a tool that makes it very easy to create Python bindings for C and C++
libraries. It was originally developed to create PyQt, the Python bindings for
the Qt toolkit, but can be used to create bindings for any C or C++ library.

SIP comprises a code generator and a Python module. The code generator processes
a set of specification files and generates C or C++ code which is then compiled
to create the bindings extension module. The SIP Python module provides support
functions to the automatically generated code.

%package -n     python3-pyqt5-sip
Summary:        Python 3/C++ Bindings Generator for pyqt5
BuildRequires:  python3-devel
Provides:       python3-pyqt5-sip-api(12) = 12.5 python3-pyqt5-sip-api(12) = 12.5

%description -n python3-pyqt5-sip
This is the Python 3 build of pyqt5-SIP.

SIP is a tool that makes it very easy to create Python bindings for C and C++
libraries. It was originally developed to create PyQt, the Python bindings for
the Qt toolkit, but can be used to create bindings for any C or C++ library.

SIP comprises a code generator and a Python module. The code generator processes
a set of specification files and generates C or C++ code which is then compiled
to create the bindings extension module. The SIP Python module provides support
functions to the automatically generated code.

%prep
%autosetup -n %{name}-%{version} -p1
%build
install -d %{_target_platform}-python3
cd %{_target_platform}-python3
%{__python3} ../configure.py CXXFLAGS+="%{optflags}" CFLAGS+="%{optflags}" LFLAGS+="%{?__global_ldflags}"
%make_build
cd -
install -d %{_target_platform}-python3-pyqt4
cd %{_target_platform}-python3-pyqt4
%{__python3} ../configure.py --sip-module=PyQt4.sip CXXFLAGS+="%{optflags}" CFLAGS+="%{optflags}" LFLAGS+="%{?__global_ldflags}"
%make_build
cd -
install -d %{_target_platform}-python3-pyqt5
cd %{_target_platform}-python3-pyqt5
%{__python3} ../configure.py --sip-module=PyQt5.sip CXXFLAGS+="%{optflags}" CFLAGS+="%{optflags}" LFLAGS+="%{?__global_ldflags}"
%make_build
cd -
%install
%make_install -C %{_target_platform}-python3
ln -s sip %{buildroot}%{_bindir}/python3-sip
%make_install -C %{_target_platform}-python3-pyqt4
%make_install -C %{_target_platform}-python3-pyqt5
install -d %{buildroot}%{python3_sitearch}/__pycache__/exclude_rpm_hack
install %{SOURCE2} %{buildroot}%{_bindir}/sip-pyqt4
install %{SOURCE2} %{buildroot}%{_bindir}/sip-pyqt5
sed -i -e 's|@SIP_MODULE@|PyQt4.sip|g' %{buildroot}%{_bindir}/sip-pyqt4
sed -i -e 's|@SIP_MODULE@|PyQt5.sip|g' %{buildroot}%{_bindir}/sip-pyqt5
install -d %{buildroot}%{_datadir}/sip
install -D -p -m644 %{SOURCE1} %{buildroot}%{rpm_macros_dir}/macros.sip

%files
%doc README LICENSE LICENSE-GPL2 LICENSE-GPL3
%{_bindir}/sip
%{_bindir}/sip-pyqt4
%{_bindir}/sip-pyqt5
%{_bindir}/python3-sip
%dir %{_datadir}/sip/
%{rpm_macros_dir}/macros.sip

%files -n python3-sip-devel
%{python3_inc}/sip.h
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
%{python3_sitearch}/PyQt4/sip.*
%{python3_sitearch}/PyQt4_sip-%{version}.dist-info/

%files -n python3-pyqt5-sip
%doc NEWS README LICENSE LICENSE-GPL2 LICENSE-GPL3
%{python3_sitearch}/PyQt5/sip.*
%{python3_sitearch}/PyQt5_sip-%{version}.dist-info/

%changelog
* Tue Jan 05 2021 maminjie <maminjie1@huawei.com> - 4.19.12-12
- resolve installation conflicts of sub-packages
- fix license

* Wed Oct 21 2020 wutao <wutao61@huawei.com> - 4.19.12-11
- delete python2 modules

* Thu Nov 28 2019 Ling Yang <lingyang2@huawei.com> - 4.19.12-10
- Package init
