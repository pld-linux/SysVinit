Summary:	System V initialization program
Summary(de):	System V-Intialisierungsprogramm
Summary(fr):	Programme d'initialisation Sys V
Summary(pl):	Program inicjalizuj±cy w Systemie V 
Summary(tr):	System V baþlatma programý
Name:		SysVinit
Version:	2.81
Release:	2
License:	GPL
Group:		Base
Group(de):	Gründsätzlich
Group(es):	Base
Group(pl):	Podstawowe
Group(pt_BR):	Base
Source0:	ftp://ftp.cistron.nl/pub/people/miquels/software/sysvinit-%{version}.tar.gz
Source1:	sysvinit.logrotate
Patch0:		sysvinit-paths.patch
Patch1:		sysvinit-bequiet.patch
Patch2:		sysvinit-md5-bigendian.patch
Patch3:		sysvinit-wtmp.patch
Patch4:		sysvinit-man.patch
Patch5:		sysvinit-halt.patch
Patch6:		sysvinit-blowfish.patch
BuildRequires:	glibc-devel
Prereq:		shadow
Prereq:		make
Prereq:		/bin/awk
Requires:	logrotate
Requires:	mingetty
Requires:	login
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir		/sbin

%description
The SysVinit package contains a group of processes that control the
very basic functions of your system. SysVinit includes the init
program, the first program started by the Linux kernel when the system
boots. Init then controls the startup, running and shutdown of all
other programs.

%description -l de
SysVinit ist das erste Programm, das beim Systemstart vom Linux-Kernel
gestartet wird. Es steuert das Starten, Ausführen und Beenden aller
anderen Programme.

%description -l fr
SysVinit est le premier programme exécuté par le noyau de Linux
lorsque le système démarre, il contrôle le lancement, l'exécution et
l'arrêt de tous les autres programmes.

%description -l pl
SysVinit jest pierwszym programem uruchamianym przez j±dro podczas
startu systemu. Kontroluje start, pracê oraz zamykanie wszystkich
innych programów.

%description -l tr
SysVinit, sistem açýlýrken Linux çekirdeði tarafýndan çalýþtýrýlan ilk
programdýr. Diðer programlarýn baþlamalarýný, çalýþmalarýný ve
sonlanmalarýný saðlar/denetler.

%prep
%setup -q -n sysvinit-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
%{__make} -C src LCRYPT="-lcrypt" \
	OPTIMIZE="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man{1,5,8}} \
	$RPM_BUILD_ROOT/{etc/{logrotate.d,sysconfig},var/log}

%{__make} install -C src \
	ROOT=$RPM_BUILD_ROOT \
	BIN_OWNER=`id -u` \
	BIN_GROUP=`id -g`

install %{SOURCE1} $RPM_BUILD_ROOT/etc/logrotate.d/sysvinit

ln -sf ../var/run/initrunlvl $RPM_BUILD_ROOT%{_sysconfdir}
ln -sf killall5 $RPM_BUILD_ROOT%{_sbindir}/pidof

touch $RPM_BUILD_ROOT{/var/log/{lastlog,wtmpx,btmpx},%{_sysconfdir}/ioctl.save}

rm -f $RPM_BUILD_ROOT%{_mandir}/man8/poweroff.8
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/telinit.8
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/reboot.8

echo .so halt.8 > $RPM_BUILD_ROOT%{_mandir}/man8/reboot.8
echo .so init.8 > $RPM_BUILD_ROOT%{_mandir}/man8/telinit.8
echo .so halt.8 > $RPM_BUILD_ROOT%{_mandir}/man8/poweroff.8
echo .so last.1 > $RPM_BUILD_ROOT%{_mandir}/man1/lastb.1

gzip -9nf doc/{Propaganda,Changelog,*.lsm}

%pre
groupadd -f -r -g 22 utmp

%post
%{_sbindir}/telinit u || :

%postun
if [ "$1" = "0" ]; then
	groupdel utmp
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/*.gz

%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_bindir}/last
%attr(755,root,root) %{_bindir}/lastb
%attr(755,root,root) %{_bindir}/mesg
%attr(755,root,root) %{_bindir}/utmpx-dump
%attr(2555,root,tty) %{_bindir}/wall

%attr(640,root,root) /etc/logrotate.d/*
%ghost %{_sysconfdir}/initrunlvl
%attr(600,root,root) %ghost %{_sysconfdir}/ioctl.save
%attr(660,root,utmp) %ghost /var/log/lastlog
%attr(660,root,utmp) %ghost /var/log/wtmpx
%attr(640,root,root) %ghost /var/log/btmpx

%{_mandir}/man*/*
