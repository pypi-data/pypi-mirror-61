Name: libluksde
Version: 20200205
Release: 1
Summary: Library to access the Linux Unified Key Setup (LUKS) Disk Encryption format
Group: System Environment/Libraries
License: LGPL
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libluksde
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:         openssl        
BuildRequires: gcc         openssl-devel        

%description -n libluksde
Library to access the Linux Unified Key Setup (LUKS) Disk Encryption format

%package -n libluksde-static
Summary: Library to access the Linux Unified Key Setup (LUKS) Disk Encryption format
Group: Development/Libraries
Requires: libluksde = %{version}-%{release}

%description -n libluksde-static
Static library version of libluksde.

%package -n libluksde-devel
Summary: Header files and libraries for developing applications for libluksde
Group: Development/Libraries
Requires: libluksde = %{version}-%{release}

%description -n libluksde-devel
Header files and libraries for developing applications for libluksde.

%package -n libluksde-python2
Obsoletes: libluksde-python < %{version}
Provides: libluksde-python = %{version}
Summary: Python 2 bindings for libluksde
Group: System Environment/Libraries
Requires: libluksde = %{version}-%{release} python2
BuildRequires: python2-devel

%description -n libluksde-python2
Python 2 bindings for libluksde

%package -n libluksde-python3
Summary: Python 3 bindings for libluksde
Group: System Environment/Libraries
Requires: libluksde = %{version}-%{release} python3
BuildRequires: python3-devel

%description -n libluksde-python3
Python 3 bindings for libluksde

%package -n libluksde-tools
Summary: Several tools for reading Linux Unified Key Setup (LUKS) Disk Encryption volumes
Group: Applications/System
Requires: libluksde = %{version}-%{release} fuse-libs
BuildRequires: fuse-devel

%description -n libluksde-tools
Several tools for reading Linux Unified Key Setup (LUKS) Disk Encryption volumes

%prep
%setup -q

%build
%configure --prefix=/usr --libdir=%{_libdir} --mandir=%{_mandir} --enable-python2 --enable-python3
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -n libluksde
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.so.*

%files -n libluksde-static
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.a

%files -n libluksde-devel
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/libluksde.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libluksde-python2
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python2*/site-packages/*.a
%{_libdir}/python2*/site-packages/*.la
%{_libdir}/python2*/site-packages/*.so

%files -n libluksde-python3
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.la
%{_libdir}/python3*/site-packages/*.so

%files -n libluksde-tools
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%changelog
* Mon Feb 10 2020 Joachim Metz <joachim.metz@gmail.com> 20200205-1
- Auto-generated

