Name:       pkgconfig
Summary:    A tool for determining compilation options
Version:    0.27.1
Release:    2
Group:      Development/Tools
License:    GPLv2+
URL:        http://pkgconfig.freedesktop.org
Source0:    http://www.freedesktop.org/software/pkgconfig/releases/pkg-config-%{version}.tar.gz
Patch0:     pkgconfig-aarch64.patch
Provides:   pkgconfig(pkg-config) = %{version}

%description
The pkgconfig tool determines compilation options. For each required
library, it reads the configuration file and outputs the necessary
compiler and linker flags.

%package doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{version}-%{release}

%description doc
Man pages for %{name}.

%prep
%setup -q -n pkg-config-%{version}
%patch0 -p1

%build

%configure --disable-static \
    --disable-shared \
    --with-internal-glib \
    --with-pc-path=%{_libdir}/pkgconfig:%{_datadir}/pkgconfig

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pkgconfig

mv $RPM_BUILD_ROOT%{_docdir}/{pkg-config,%{name}-%{version}}
install -m0644 -t $RPM_BUILD_ROOT%{_docdir}/pkgconfig-%{version} \
        AUTHORS README NEWS

%files
%defattr(-,root,root,-)
%license COPYING
%{_bindir}/*
%{_libdir}/pkgconfig
%{_datadir}/pkgconfig
%{_datadir}/aclocal/*

%files doc
%defattr(-,root,root,-)
%{_mandir}/man1/pkg-config.*
%{_docdir}/%{name}-%{version}
