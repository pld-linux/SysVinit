#
# Conditional build:
%bcond_with	preconfigured
%bcond_without	selinux		# build without SELinux support

Summary:	System V initialization program
Summary(de.UTF-8):	System V-Intialisierungsprogramm
Summary(es.UTF-8):	Programa de inicialización System V
Summary(fr.UTF-8):	Programme d'initialisation Sys V
Summary(pl.UTF-8):	Program inicjalizujący w Systemie V
Summary(pt_BR.UTF-8):	Programa de inicialização System V
Summary(ru.UTF-8):	Программы, управляющие базовыми системными процессами
Summary(tr.UTF-8):	System V başlatma programı
Summary(uk.UTF-8):	Програми, що керують базовими системними процесами
Name:		SysVinit
Version:	2.88
Release:	5
License:	GPL
Group:		Base
Source0:	http://download.savannah.gnu.org/releases/sysvinit/sysvinit-%{version}dsf.tar.bz2
# Source0-md5:	6eda8a97b86e0a6f59dabbf25202aa6f
Source1:	sysvinit.logrotate
Source2:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/sysvinit-non-english-man-pages.tar.bz2
# Source2-md5:	9ae8a63a4685368fae19707f95475cca
Patch0:		sysvinit-paths.patch
Patch1:		sysvinit-bequiet.patch
Patch2:		sysvinit-wtmp.patch
Patch3:		sysvinit-man.patch
Patch4:		sysvinit-halt.patch
Patch5:		sysvinit-autofsck.patch
Patch6:		sysvinit-pidof.patch
Patch7:		sysvinit-killall5.patch
Patch8:		sysvinit-nopowerstates-single.patch
Patch9:		sysvinit-lastlog.patch
Patch10:	sysvinit-alt-fixes.patch
Patch11:	sysvinit-quiet.patch
Patch12:	sysvinit-rebootconfirmation.patch
%if %{with selinux}
BuildRequires:	libselinux-devel >= 1.28
BuildRequires:	libsepol-devel
%endif
BuildRequires:	rpmbuild(macros) >= 1.202
Requires(postun):	/usr/sbin/groupdel
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires:	%{name}-tools = %{version}-%{release}
Requires:	/bin/awk
%{?with_selinux:Requires:	libselinux >= 1.18}
Requires:	login
Requires:	mingetty
Requires:	util-linux >= 2.20-5
Provides:	group(utmp)
Provides:	virtual(init-daemon)
Obsoletes:	upstart-SysVinit
#Obsoletes:	virtual(init-daemon)
Obsoletes:	vserver-SysVinit
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin
# as in original flags
%define		specflags	-fomit-frame-pointer

%description
The SysVinit package contains a group of processes that control the
very basic functions of your system. SysVinit includes the init
program, the first program started by the Linux kernel when the system
boots. Init then controls the startup, running and shutdown of all
other programs.

%description -l de.UTF-8
SysVinit ist das erste Programm, das beim Systemstart vom Linux-Kernel
gestartet wird. Es steuert das Starten, Ausführen und Beenden aller
anderen Programme.

%description -l es.UTF-8
SysVinit es el primer programa ejecutado por el kernel Linux cuando se
inicia el sistema. Controla arranque, funcionamiento y cierre de todos
los otros programas.

%description -l fr.UTF-8
SysVinit est le premier programme exécuté par le noyau de Linux
lorsque le système démarre, il contrôle le lancement, l'exécution et
l'arrêt de tous les autres programmes.

%description -l pl.UTF-8
SysVinit jest pierwszym programem uruchamianym przez jądro podczas
startu systemu. Kontroluje start, pracę oraz zamykanie wszystkich
innych programów.

%description -l pt_BR.UTF-8
SysVinit é o primeiro programa executado pelo kernel Linux quando o
sistema é inicializado. Controla inicialização, funcionamento e
finalização de todos os outros programas.

%description -l ru.UTF-8
Пакет SysVinit содержит группу процессов, которые управляют самыми
базовыми функциями вашей системы. SysVinit включает программу init,
самую первую программу, которая запускается ядром Linux при загрузке
системы. После этого init управляет запуском, исполнением и остановом
всех остальных программ.

%description -l tr.UTF-8
SysVinit, sistem açılırken Linux çekirdeği tarafından çalıştırılan ilk
programdır. Diğer programların başlamalarını, çalışmalarını ve
sonlanmalarını sağlar/denetler.

%description -l uk.UTF-8
Пакет SysVinit містить групу процесів, котрі керують самими базовими
функціями вашої системи. SysVinit містить програму init, першу
програму, яку запускає ядро Linux під час загрузки системи. Після
цього init керує запуском, виконанням та зупинкою всіх інших програм.

%package tools
Summary:	Tools used for process and utmp management
Group:		Base
Conflicts:	SysVinit < 2.86-27
Conflicts:	rc-scripts < 0.4.5.1-6

%description tools
The sysvinit-tools package contains various tools used for process
management.

%prep
%setup -q -n sysvinit-%{version}dsf
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p0

%build
%{__make} -C src \
	%{?with_selinux:WITH_SELINUX=yes} \
	CC="%{__cc}" \
	LCRYPT="-lcrypt" \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/bin,%{_bindir},%{_sbindir},%{_mandir}/man{1,5,8}} \
	$RPM_BUILD_ROOT{%{_includedir},%{_sysconfdir},/etc/logrotate.d,/var/{log,run}}

%{__make} install -C src \
	ROOT=$RPM_BUILD_ROOT \
	BIN_OWNER=`id -u` \
	BIN_GROUP=`id -g`

install %{SOURCE1} $RPM_BUILD_ROOT/etc/logrotate.d/sysvinit

ln -s ../var/run/initrunlvl $RPM_BUILD_ROOT%{_sysconfdir}
ln -s killall5 $RPM_BUILD_ROOT%{_sbindir}/pidof
ln -s utmpdump $RPM_BUILD_ROOT%{_bindir}/utmpx-dump

> $RPM_BUILD_ROOT%{_sysconfdir}/ioctl.save
> $RPM_BUILD_ROOT/var/log/btmpx
> $RPM_BUILD_ROOT/var/log/faillog
> $RPM_BUILD_ROOT/var/log/lastlog
> $RPM_BUILD_ROOT/var/log/wtmpx
> $RPM_BUILD_ROOT/var/run/initrunlvl

echo .so last.1 > $RPM_BUILD_ROOT%{_mandir}/man1/lastb.1
echo .so utmpdump.1 > $RPM_BUILD_ROOT%{_mandir}/man1/utmpx-dump.1
echo .so halt.8 > $RPM_BUILD_ROOT%{_mandir}/man8/poweroff.8
echo .so halt.8 > $RPM_BUILD_ROOT%{_mandir}/man8/reboot.8
echo .so init.8 > $RPM_BUILD_ROOT%{_mandir}/man8/telinit.8
bzip2 -dc %{SOURCE2} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}
%{__rm} $RPM_BUILD_ROOT%{_includedir}/initreq.h
%{__rm} $RPM_BUILD_ROOT%{_mandir}/README.sysvinit-non-english-man-pages

cp -a man/intl/* $RPM_BUILD_ROOT%{_mandir}

# in util-linux
rm $RPM_BUILD_ROOT{/bin/mountpoint,%{_mandir}/man1/mountpoint.1*}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 22 utmp

%post
touch %{_sysconfdir}/ioctl.save /var/log/{btmpx,{fail,last}log}
chmod 000 %{_sysconfdir}/ioctl.save /var/log/{fail,last}log
chown root:root %{_sysconfdir}/ioctl.save /var/log/faillog
chown root:utmp /var/log/lastlog
chmod 600 %{_sysconfdir}/ioctl.save
chmod 640 /var/log/btmpx
chmod 640 /var/log/faillog
chmod 664 /var/log/lastlog
if [ -p /dev/initctl ]; then
	%{_sbindir}/telinit u || :
fi

%triggerpostun -- glibc
if [ -p /dev/initctl ]; then
	%{_sbindir}/telinit u || :
fi

%postun
if [ "$1" = "0" ]; then
	%groupremove utmp
fi

%files
%defattr(644,root,root,755)
%doc doc/{Propaganda,Changelog,*.lsm} src/initscript.sample

%attr(755,root,root) %{_sbindir}/bootlogd
%attr(755,root,root) %{_sbindir}/halt
%attr(755,root,root) %{_sbindir}/init
%attr(755,root,root) %{_sbindir}/poweroff
%attr(755,root,root) %{_sbindir}/reboot
%attr(755,root,root) %{_sbindir}/runlevel
%attr(755,root,root) %{_sbindir}/shutdown
%attr(755,root,root) %{_sbindir}/telinit
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/sysvinit
%ghost %{_sysconfdir}/initrunlvl
%ghost /var/run/initrunlvl
%attr(600,root,root) %ghost %{_sysconfdir}/ioctl.save
%attr(640,root,root) %ghost /var/log/btmpx
%attr(664,root,utmp) %ghost /var/log/wtmpx

%{_mandir}/man5/inittab.5*
%{_mandir}/man5/initscript.5*
%{_mandir}/man8/bootlogd.8*
%{_mandir}/man8/halt.8*
%{_mandir}/man8/init.8*
%{_mandir}/man8/lastlog.8*
%{_mandir}/man8/poweroff.8
%{_mandir}/man8/reboot.8
%{_mandir}/man8/runlevel.8*
%{_mandir}/man8/shutdown.8*
%{_mandir}/man8/telinit.8
%lang(de) %{_mandir}/de/man8/init.8*
%lang(de) %{_mandir}/de/man8/telinit.8
%lang(es) %{_mandir}/es/man5/initscript.5*
%lang(es) %{_mandir}/es/man5/inittab.5*
%lang(es) %{_mandir}/es/man8/halt.8*
%lang(es) %{_mandir}/es/man8/init.8*
%lang(es) %{_mandir}/es/man8/poweroff.8
%lang(es) %{_mandir}/es/man8/reboot.8
%lang(es) %{_mandir}/es/man8/runlevel.8*
%lang(es) %{_mandir}/es/man8/shutdown.8*
%lang(es) %{_mandir}/es/man8/telinit.8
%lang(fr) %{_mandir}/fr/man8/halt.8*
%lang(fr) %{_mandir}/fr/man8/reboot.8
%lang(fr) %{_mandir}/fr/man8/runlevel.8*
%lang(fr) %{_mandir}/fr/man8/shutdown.8*
%lang(hu) %{_mandir}/hu/man5/inittab.5*
%lang(hu) %{_mandir}/hu/man8/init.8*
%lang(hu) %{_mandir}/hu/man8/shutdown.8*
%lang(hu) %{_mandir}/hu/man8/telinit.8
%lang(id) %{_mandir}/id/man8/halt.8*
%lang(id) %{_mandir}/id/man8/reboot.8
%lang(id) %{_mandir}/id/man8/shutdown.8*
%lang(it) %{_mandir}/it/man5/initscript.5*
%lang(it) %{_mandir}/it/man5/inittab.5*
%lang(it) %{_mandir}/it/man8/halt.8*
%lang(it) %{_mandir}/it/man8/init.8*
%lang(it) %{_mandir}/it/man8/reboot.8
%lang(it) %{_mandir}/it/man8/runlevel.8*
%lang(it) %{_mandir}/it/man8/shutdown.8*
%lang(it) %{_mandir}/it/man8/telinit.8
%lang(ja) %{_mandir}/ja/man5/initscript.5*
%lang(ja) %{_mandir}/ja/man5/inittab.5*
%lang(ja) %{_mandir}/ja/man8/halt.8*
%lang(ja) %{_mandir}/ja/man8/init.8*
%lang(ja) %{_mandir}/ja/man8/poweroff.8
%lang(ja) %{_mandir}/ja/man8/reboot.8
%lang(ja) %{_mandir}/ja/man8/runlevel.8*
%lang(ja) %{_mandir}/ja/man8/shutdown.8*
%lang(ja) %{_mandir}/ja/man8/telinit.8
%lang(ko) %{_mandir}/ko/man5/initscript.5*
%lang(ko) %{_mandir}/ko/man5/inittab.5*
%lang(ko) %{_mandir}/ko/man8/halt.8*
%lang(ko) %{_mandir}/ko/man8/init.8*
%lang(ko) %{_mandir}/ko/man8/reboot.8
%lang(ko) %{_mandir}/ko/man8/runlevel.8*
%lang(ko) %{_mandir}/ko/man8/shutdown.8*
%lang(ko) %{_mandir}/ko/man8/telinit.8
%lang(pl) %{_mandir}/pl/man5/initscript.5*
%lang(pl) %{_mandir}/pl/man5/inittab.5*
%lang(pl) %{_mandir}/pl/man8/halt.8*
%lang(pl) %{_mandir}/pl/man8/init.8*
%lang(pl) %{_mandir}/pl/man8/poweroff.8
%lang(pl) %{_mandir}/pl/man8/reboot.8
%lang(pl) %{_mandir}/pl/man8/runlevel.8*
%lang(pl) %{_mandir}/pl/man8/shutdown.8*
%lang(pl) %{_mandir}/pl/man8/telinit.8

# devel?
#%{_includedir}/initreq.h

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) /bin/pidof
%attr(755,root,root) %{_sbindir}/fstab-decode
%attr(755,root,root) %{_sbindir}/killall5
%attr(755,root,root) %{_sbindir}/lastlog
%attr(755,root,root) %{_sbindir}/pidof
%attr(755,root,root) %{_sbindir}/sulogin
%attr(755,root,root) %{_bindir}/last
%attr(755,root,root) %{_bindir}/lastb
%attr(755,root,root) %{_bindir}/mesg
%attr(755,root,root) %{_bindir}/utmpdump
%attr(755,root,root) %{_bindir}/utmpx-dump
%attr(755,root,root) %{_bindir}/wall
%attr(640,root,root) %ghost /var/log/faillog
%attr(664,root,utmp) %ghost /var/log/lastlog
%{_mandir}/man1/last.1*
%{_mandir}/man1/lastb.1*
%{_mandir}/man1/mesg.1*
%{_mandir}/man1/wall.1*
%{_mandir}/man1/utmpdump.1*
%{_mandir}/man1/utmpx-dump.1*
%{_mandir}/man8/killall5.8*
%{_mandir}/man8/pidof.8*
%{_mandir}/man8/sulogin.8*
%{_mandir}/man8/fstab-decode.8*
%lang(cs) %{_mandir}/cs/man8/lastlog.8*
%lang(es) %{_mandir}/es/man1/last.1*
%lang(es) %{_mandir}/es/man1/lastb.1
%lang(es) %{_mandir}/es/man1/mesg.1*
%lang(es) %{_mandir}/es/man1/wall.1*
%lang(es) %{_mandir}/es/man8/killall5.8*
%lang(es) %{_mandir}/es/man8/pidof.8*
%lang(es) %{_mandir}/es/man8/sulogin.8*
%lang(fi) %{_mandir}/fi/man1/last.1*
%lang(fi) %{_mandir}/fi/man1/mesg.1*
%lang(fi) %{_mandir}/fi/man1/wall.1*
%lang(fr) %{_mandir}/fr/man1/last.1*
%lang(fr) %{_mandir}/fr/man1/mesg.1*
%lang(fr) %{_mandir}/fr/man1/wall.1*
%lang(fr) %{_mandir}/fr/man8/killall5.8*
%lang(fr) %{_mandir}/fr/man8/lastlog.8*
%lang(fr) %{_mandir}/fr/man8/pidof.8*
%lang(hu) %{_mandir}/hu/man1/last.1*
%lang(hu) %{_mandir}/hu/man1/mesg.1*
%lang(hu) %{_mandir}/hu/man1/wall.1*
%lang(hu) %{_mandir}/hu/man8/lastlog.8*
%lang(it) %{_mandir}/it/man1/last.1*
%lang(it) %{_mandir}/it/man1/lastb.1
%lang(it) %{_mandir}/it/man1/mesg.1*
%lang(it) %{_mandir}/it/man1/wall.1*
%lang(it) %{_mandir}/it/man8/killall5.8*
%lang(it) %{_mandir}/it/man8/lastlog.8*
%lang(it) %{_mandir}/it/man8/pidof.8*
%lang(it) %{_mandir}/it/man8/sulogin.8*
%lang(ja) %{_mandir}/ja/man1/last.1*
%lang(ja) %{_mandir}/ja/man1/lastb.1
%lang(ja) %{_mandir}/ja/man1/mesg.1*
%lang(ja) %{_mandir}/ja/man1/wall.1*
%lang(ja) %{_mandir}/ja/man8/killall5.8*
%lang(ja) %{_mandir}/ja/man8/lastlog.8*
%lang(ja) %{_mandir}/ja/man8/pidof.8*
%lang(ja) %{_mandir}/ja/man8/sulogin.8*
%lang(ko) %{_mandir}/ko/man1/last.1*
%lang(ko) %{_mandir}/ko/man1/lastb.1
%lang(ko) %{_mandir}/ko/man1/mesg.1*
%lang(ko) %{_mandir}/ko/man8/killall5.8*
%lang(ko) %{_mandir}/ko/man8/pidof.8*
%lang(ko) %{_mandir}/ko/man8/sulogin.8*
%lang(pl) %{_mandir}/pl/man1/last.1*
%lang(pl) %{_mandir}/pl/man1/lastb.1
%lang(pl) %{_mandir}/pl/man1/mesg.1*
%lang(pl) %{_mandir}/pl/man1/wall.1*
%lang(pl) %{_mandir}/pl/man8/killall5.8*
%lang(pl) %{_mandir}/pl/man8/lastlog.8*
%lang(pl) %{_mandir}/pl/man8/pidof.8*
%lang(pl) %{_mandir}/pl/man8/sulogin.8*
%lang(ru) %{_mandir}/ru/man8/lastlog.8*
%lang(sv) %{_mandir}/sv/man8/lastlog.8*
