Summary:	System V initialization program
Summary(de):	System V-Intialisierungsprogramm
Summary(fr):	Programme d'initialisation Sys V.
Summary(pl):	Program inicjalizuj±cy w Systemie V 
Summary(tr):	System V baþlatma programý
Name:		SysVinit
Version:	2.78
Release:	5
License:	GPL
Group:		Base
Group(pl):	Podstawowe
Source0:	ftp://ftp.cistron.nl/pub/people/miquels/software/sysvinit-%{version}.tar.gz
Source1:	sysvinit.logrotate
Patch0:		sysvinit-paths.patch
Patch1:		sysvinit-bequiet.patch
Patch2:		sysvinit-md5-bigendian.patch
Patch3:		sysvinit-wtmpx.patch
Prereq:		fileutils
Prereq:		utempter
Requires:	logrotate
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
The SysVinit package contains a group of processes that control the very
basic functions of your system. SysVinit includes the init program, the
first program started by the Linux kernel when the system boots. Init then
controls the startup, running and shutdown of all other programs.

%description -l de
SysVinit ist das erste Programm, das beim Systemstart vom Linux-Kernel
gestartet wird. Es steuert das Starten, Ausführen und Beenden aller anderen
Programme.

%description -l fr
SysVinit est le premier programme exécuté par le noyau de Linux lorsque le
système démarre, il contrôle le lancement, l'exécution et l'arrêt de tous
les autres programmes.

%description -l pl
SysVinit jest pierwszym programem uruchamianym przez j±dro, podczas  startu
systemu. Kontroluje start, pracê oraz zamykanie wszystkich innych
programów.

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

%build
make -C src OPTIMIZE="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man{1,5,8}} \
	$RPM_BUILD_ROOT/{etc/{logrotate.d,sysconfig},var/log}

make install -C src \
	ROOT=$RPM_BUILD_ROOT \
	BIN_OWNER=`id -u` \
	BIN_GROUP=`id -g`

install %{SOURCE1} $RPM_BUILD_ROOT/etc/logrotate.d/sysvinit

ln -sf ../var/run/initrunlvl $RPM_BUILD_ROOT/etc
ln -sf killall5 $RPM_BUILD_ROOT%{_sbindir}/pidof

touch $RPM_BUILD_ROOT/var/log/{lastlog,wtmpx,btmpx}

rm -f $RPM_BUILD_ROOT%{_mandir}/man8/poweroff.8
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/telinit.8
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/reboot.8

echo .so halt.8 > $RPM_BUILD_ROOT%{_mandir}/man8/reboot.8
echo .so halt.8 > $RPM_BUILD_ROOT%{_mandir}/man8/telinit.8
echo .so halt.8 > $RPM_BUILD_ROOT%{_mandir}/man8/poweroff.8
echo .so last.1 > $RPM_BUILD_ROOT%{_mandir}/man1/lastb.1

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* \
	doc/Propaganda debian/changelog doc/sysvinit-%{version}.lsm  

%post
if [ -f /var/log/wtmp ]; then
	mv -f /var/log/wtmp /var/log/wtmp.rpmsave
fi
touch /var/log/{lastlog,wtmpx,btmpx}
chmod 0644 /var/log/lastlog /var/log/wtmpx
chmod 0640 /var/log/btmpx
chgrp utmp /var/log/wtmpx

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/Propaganda.gz debian/changelog.gz doc/sysvinit-%{version}.lsm.gz

%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_bindir}/last
%attr(755,root,root) %{_bindir}/lastb
%attr(755,root,root) %{_bindir}/mesg
%attr(755,root,root) %{_bindir}/utmpx-dump
%attr(2555,root,tty) %{_bindir}/wall

%attr(640,root,root) /etc/logrotate.d/*
%ghost /etc/initrunlvl
%ghost /var/log/lastlog
%attr(660,root,utmp) %ghost /var/log/wtmpx
%attr(640,root,root) %ghost /var/log/btmpx

%{_mandir}/man*/*
