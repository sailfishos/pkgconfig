Name:       pkgconfig
Summary:    A tool for determining compilation options
Version:    0.29.2
Release:    2
Group:      Development/Tools
License:    GPLv2+
URL:        http://pkgconfig.freedesktop.org
Source0:    http://www.freedesktop.org/software/pkgconfig/releases/pkgconfig-%{version}.tar.gz
Patch0:     0001-Tolerate-gettext-being-installed.patch
Provides:   pkgconfig(pkg-config) = %{version}
# This build uses the likes of autoconf, automake, and libtool, but adding them as
# build deps would cause superfluous build loops. 

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
%setup -q -n %{name}-%{version}/upstream
%autopatch -p1

%build
NOCONFIGURE=1 ./autogen.sh
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
