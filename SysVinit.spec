Summary:	System V initialization program
Summary(de):	System V-Intialisierungsprogramm
Summary(fr):	Programme d'initialisation Sys V.
Summary(pl):	Program inicjalizuj±cy w Systemie V 
Summary(tr):	System V baþlatma programý
Name:		SysVinit
Version:	2.76
Release:	9
Copyright:	GPL
Group:		Base
Group(pl):	Bazowe
Source0:	ftp://ftp.cistron.nl/pub/people/miquels/software/sysvinit-%{version}.tar.gz
Source1:	sysvinit-initscript
Patch0:		sysvinit-optimize.patch
Patch1:		sysvinit-FHS2.patch
Requires:	/dev/initctl
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

install -d $RPM_BUILD_ROOT/{sbin,etc,dev,var/run,usr/{bin,share/man/man{1,5,8}}}

make install -C src \
	ROOT=$RPM_BUILD_ROOT \
	BIN_OWNER=`id -u` \
	BIN_GROUP=`id -g`
install %{SOURCE1} $RPM_BUILD_ROOT/etc/initscript

ln -sf ../var/run/initrunlvl $RPM_BUILD_ROOT/etc

ln -sf killall5 $RPM_BUILD_ROOT/sbin/pidof

# man pages cleaning & compressing ;)

rm -f $RPM_BUILD_ROOT/usr/share/man/man1/lastb.1

echo .so last.1 > $RPM_BUILD_ROOT/usr/share/man/man1/lastb.1

rm -f $RPM_BUILD_ROOT/usr/share/man/man8/poweroff.8
rm -f $RPM_BUILD_ROOT/usr/share/man/man8/telinit.8
rm -f $RPM_BUILD_ROOT/usr/share/man/man8/reboot.8

echo .so halt.8 > $RPM_BUILD_ROOT/usr/share/man/man8/reboot.8
echo .so halt.8 > $RPM_BUILD_ROOT/usr/share/man/man8/telinit.8
echo .so halt.8 > $RPM_BUILD_ROOT/usr/share/man/man8/poweroff.8

gzip -9nf $RPM_BUILD_ROOT/usr/share/man/man*/* \
	doc/Propaganda debian/changelog doc/sysvinit-%{version}.lsm  

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/Propaganda.gz debian/changelog.gz doc/sysvinit-%{version}.lsm.gz  

%attr(755,root,root) /sbin/*

#%ghost /etc/*

%attr(755,root,root) /usr/bin/*
#%attr(600,root,root) /dev/initctl
%attr(640,root,root) /etc/initscript
/usr/share/man/man[158]/*

%changelog
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
- added a Chris Evans's <chris@ferret.lmh.ox.ac.uk> patches.

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 2.74
- fixed the package source url... (yeah, it was wrong !)

* Wed Oct 1 1997 Cristian Gafton <gafton@redhat.com>
- fixed the MD5 check in sulogin (128 hash bits encoded with base64 gives
  22 bytes, not 24...). Fix in -md5.patch

* Thu Sep 11 1997 Christian 'Dr. Disk' Hechelmann <drdisk@ds9.au.s.shuttle.de>
- /etc/initrunlvl gets linked to /tmp/init-root/var/run/initrunlvl which is
  just plain wrong..
- /usr/bin/utmpdump was missing in the files section, although it was
  explicitly patched into PROGS.
- added attr's to the files section.
- various small fixes.

* Tue Jun 17 1997 Erik Troan <ewt@redhat.com>
- updated to 2.71
- built against glibc 2.0.4

* Fri Feb 07 1997 Michael K. Johnson <johnsonm@redhat.com>
- Added sulogin.8 man page to file list.
