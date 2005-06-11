Summary:	Driver and diagnostic utility for Usermode SoundModem
Summary(pl):	Sterownik i narzêdzie diagnostyczne dla SoundModemu w przestrzeni u¿ytkownika
Name:		soundmodem
Version:	0.7
Release:	1
License:	GPL
Group:		Networking
Source0:	http://www.baycom.org/~tom/ham/soundmodem/%{name}-%{version}.tar.gz
# Source0-md5:	33026c681f238f81f7657edc7d46e68a
Source1:	%{name}.init
URL:		http://www.baycom.org/~tom/ham/soundmodem/
BuildRequires:	audiofile-devel
BuildRequires:	automake
BuildRequires:	gtk+-devel
BuildRequires:	libxml-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the driver and the diagnostic utility for
userspace SoundModem. It allows you to use soundcards supported by
OSS/Free as Amateur Packet Radio modems.

%description -l pl
Ten pakiet zawiera sterownik i narzêdzie diagnostyczne dla SoundModemu
dzia³aj±cego w przestrzeni u¿ytkownika. Pozwala u¿ywaæ kart
d¼wiêkowych obs³ugiwanych przez OSS/Free jako modemy Amateur Packet
Radio.

%package X11
Summary:	GUI for soundmodem configuration
Summary(pl):	Graficzny interfejs do konfiguracji soundmodemu
Group:		X11/Applications
Requires:	%{name} = %{version}

%description X11
GUI interface for soundmodem.

%description X11 -l pl
Graficzny interfejs u¿ytkownika dla soundmodemu.

%prep
%setup -q

%build
install /usr/share/automake/config.* .
%configure2_13 \
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

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/%{name} start\" to start %{name}." 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/%{name} ]; then
		/etc/rc.d/init.d/%{name} stop >&2
fi
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README newqpsk/README.newqpsk
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man?/soundmodem.*
%attr(754,root,root) %{_initrddir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ax25/soundmodem.conf

%files X11
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man?/soundmodemconfig.*
