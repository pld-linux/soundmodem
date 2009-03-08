Summary:	Driver and diagnostic utility for Usermode SoundModem
Summary(pl.UTF-8):	Sterownik i narzędzie diagnostyczne dla SoundModemu w przestrzeni użytkownika
Name:		soundmodem
Version:	0.12
Release:	1
License:	GPL
Group:		Networking
Source0:	http://www.baycom.org/~tom/ham/soundmodem/%{name}-%{version}.tar.gz
# Source0-md5:	b2c222cf4ae16bbdbdc85de56cf7f850
Source1:	%{name}.init
URL:		http://www.baycom.org/~tom/ham/soundmodem/
BuildRequires:	audiofile-devel
BuildRequires:	automake
BuildRequires:	gtk+-devel
BuildRequires:	libxml-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the driver and the diagnostic utility for
userspace SoundModem. It allows you to use soundcards supported by
OSS/Free as Amateur Packet Radio modems.

%description -l pl.UTF-8
Ten pakiet zawiera sterownik i narzędzie diagnostyczne dla SoundModemu
działającego w przestrzeni użytkownika. Pozwala używać kart
dźwiękowych obsługiwanych przez OSS/Free jako modemy Amateur Packet
Radio.

%package devel
Summary:        Header files for soundmodem library
Summary(pl.UTF-8):      Pliki nagłówkowe biblioteki dla soundmodem
Group:          Development/Libraries
Requires:      %{name} = %{version}-%{release}

%description devel
Header files for soundmodem library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki dla soundmodem.

%package X11
Summary:	GUI for soundmodem configuration
Summary(pl.UTF-8):	Graficzny interfejs do konfiguracji soundmodemu
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description X11
GUI interface for soundmodem.

%description X11 -l pl.UTF-8
Graficzny interfejs użytkownika dla soundmodemu.

%prep
%setup -q

%build
install /usr/share/automake/config.* .
%configure \
%ifarch i686 athlon
	--enable-mmx \
%endif
%ifarch sparc64
	--enable-vis \
%endif
# empty line
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/ax25,%{_initrddir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/%{name}
touch $RPM_BUILD_ROOT%{_sysconfdir}/ax25/soundmodem.conf

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README newqpsk/README.newqpsk
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man?/soundmodem.*
%attr(754,root,root) %{_initrddir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ax25/soundmodem.conf

%files devel
%{_includedir}/modem.h
%{_includedir}/simd.h

%files X11
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man?/soundmodemconfig.*
