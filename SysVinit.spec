Summary:	System V initialization program
Summary(de):	System V-Intialisierungsprogramm
Summary(fr):	Programme d'initialisation Sys V.
Summary(pl):	Program inicjalizuj±cy w Systemie V 
Summary(tr):	System V baþlatma programý
Name:		SysVinit
Version:	2.76
Release:	14
Copyright:	GPL
Group:		Base
Group(pl):	Podstawowe
URL:		ftp://ftp.cistron.nl/pub/people/miquels/software/
Source0:	sysvinit-%{version}.tar.gz
Source1:	sysvinit-initscript
Source2:	sysvinit.logrotate
Patch0:		sysvinit-paths.patch
Patch1:		sysvinit-man.patch
Requires:	logrotate
Buildroot:	/tmp/%{name}-%{version}-root

%description
SysVinit is the first program started by the Linux kernel when the system
boots, controlling the startup, running, and shutdown of all other
programs.

%description -l pl
SysVinit jest pierwszym programem uruchamianym przez j±dro, podczas 
startu systemu. Kontroluje start, pracê oraz zamykanie wszystkich
innych programów.

%description -l de
SysVinit ist das erste Programm, das beim Systemstart vom Linux-Kernel 
gestartet wird. Es steuert das Starten, Ausführen und Beenden aller
anderen Programme.

%description -l fr
SysVinit est le premier programme exécuté par le noyau de Linux lorsque le
système démarre, il contrôle le lancement, l'exécution et l'arrêt de tous
les autres programmes.

%description -l tr
SysVinit, sistem açýlýrken Linux çekirdeði tarafýndan çalýþtýrýlan ilk
programdýr. Diðer programlarýn baþlamalarýný, çalýþmalarýný ve sonlanmalarýný
saðlar/denetler.

%prep
%setup -q -n sysvinit-%{version}
%patch0 -p1
%patch1 -p1

%build
make -C src OPTIMIZE="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_prefix}/{bin,share/man/man{1,5,8}}
install -d $RPM_BUILD_ROOT/{sbin,etc/{logrotate.d,sysconfig},var/log}

make install -C src \
	ROOT=$RPM_BUILD_ROOT \
	BIN_OWNER=`id -u` \
	BIN_GROUP=`id -g`

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/initscript
install %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate.d/sysvinit

ln -sf ../var/run/initrunlvl $RPM_BUILD_ROOT/etc
ln -sf killall5 $RPM_BUILD_ROOT/sbin/pidof

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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/Propaganda.gz debian/changelog.gz doc/sysvinit-%{version}.lsm.gz  

%attr(755,root,root) /sbin/*
%attr(755,root,root) %{_bindir}/*

%attr(644,root,root) %config /etc/sysconfig/initscript
%attr(640,root,root) /etc/logrotate.d/*
%ghost /etc/initrunlvl
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /var/log/lastlog
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /var/log/btmpx
%config(noreplace) %verify(not size mtime md5) /var/log/wtmpx

%{_mandir}/man[158]/*

%changelog
* Sat May 22 1999 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [2.76-10]
- (u,w)tmp changed to (w,u)tmpx -- Unix98 comliant (patch),
- utpmdump changed to utmpx-dump, (patch)
- changed prefix for initscript to /etc/rc.d instead /etc (patch)
- added /etc/logrotate.d/sysvinit (for logrotate) & /var/log/lastlog,
- removed sgid bit from `wall' -- following Debian developers advise ;) 
- %ghost /etc/initrunlvl,
- added /var/log/{btmpx,wtmpx} -- removed from sysklogd package,
- fixed all patches.

* Tue May 11 1999 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [2.74-9]
- now package is FHS 2.0 compliant.

* Tue Apr 27 1999 Wojciech "Sas" Cieciwa <cieciwa@alpha.zarz.agh.edu.pl>
- removed /dev/initctl, now this is part of dev package.

* Tue Apr 20 1999 Artur Frysiak <wiget@pld.org.pl>
  [2.74-8]
- compiled on rpm 3

* Tue Feb  9 1999 Micha³ Kuratczyk <kurkens@polbox.com>
  [2.74-6d]
- gzipping instead bzipping
- cosmetic changes

* Fri Jun 12 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [2.74-5d]
- build against glibc-2.1,
- added pl translation,
- changed prmissions of binaries to 711,
- removed a suid bit from wall,
- moved %changelog at the end of spec.
- added a Chris Evans's <chris@ferret.lmh.ox.ac.uk> patches,
- start at RH spec file.
