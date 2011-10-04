Summary: A tool for determining compilation options
Name: pkgconfig
Version: 0.25
Release: 2
License: GPLv2+
URL: http://pkgconfig.freedesktop.org
Group: Development/Tools
Source:  http://www.freedesktop.org/software/pkgconfig/releases/pkg-config-%{version}.tar.gz
#BuildRequires: glib2-devel
BuildRequires: popt-devel

# don't call out to glib-config, since our glib-config is a pkg-config wrapper
Patch2:  pkg-config-0.21-compat-loop.patch
# https://bugs.freedesktop.org/show_bug.cgi?id=16095
Patch3: pkg-config-lib64-excludes.patch
# workaround for breakage with autoconf 2.66
# https://bugzilla.redhat.com/show_bug.cgi?id=611781
Patch4: pkg-config-dnl.patch

Provides: pkgconfig(pkg-config) = %{version}

%description
The pkgconfig tool determines compilation options. For each required
library, it reads the configuration file and outputs the necessary
compiler and linker flags.

%prep
%setup -n pkg-config-%{version} -q
%patch2 -p1 -b .compat-loop
%patch3 -p0 -b .lib64
%patch4 -p1 -R -b .dnl

%build
%configure \
        --disable-shared \
        --with-pc-path=%{_libdir}/pkgconfig:%{_datadir}/pkgconfig
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pkgconfig

# we include this below, already
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/pkg-config

%files
%defattr(-,root,root)
%doc AUTHORS README NEWS COPYING pkg-config-guide.html
%{_mandir}/*/*
%{_bindir}/*
%{_libdir}/pkgconfig
%{_datadir}/pkgconfig
%{_datadir}/aclocal/*

