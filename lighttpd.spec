#
# TODO
# - test ldap and mysql (failed at this time)
# - documentroot specified in config doesn't exist
# - mysql issue: http://www.freebsd.org/cgi/query-pr.cgi?pr=76866
#
# Conditional build for lighttpd:
%bcond_without	xattr		# without support of extended attributes
%bcond_with	mysql		# with mysql
%bcond_with	ldap		# with ldap
%bcond_with	valgrind	# enable valgrind fixes in code.
%bcond_without	ipv6		# IPv4-only version (doesn't require IPv6 in kernel)
%bcond_without	largefile	# without largefile support,
%bcond_without	ssl		# disable ssl support
# use it if you have 2.4 kernel to get sendfile() support,
# and don't need > 2GB file requests,
# see http://article.gmane.org/gmane.comp.web.lighttpd:722
#

# Prerelease snapshot: DATE-TIME
##define _snap 20050116-1743

%if 0%{?_snap}
%define _source http://www.lighttpd.net/download/%{name}-%{version}-%{_snap}.tar.gz
%else
%define _source http://www.lighttpd.net/download/%{name}-%{version}.tar.gz
%endif

%define		_rel 1

Summary:	Fast and light HTTP server
Summary(pl):	Szybki i lekki serwer HTTP
Name:		lighttpd
Version:	1.3.10
Release:	%{_rel}%{?_snap:.%(echo %{_snap}|tr - _)}
Group:		Networking/Daemons
License:	BSD
Source0:	%{_source}
# Source0-md5:	28623eff50653a9b104ddb20fe65aaf1
Source1:	%{name}.init
Source2:	%{name}.conf
Source3:	%{name}.user
Source4:	%{name}.logrotate
Source5:	%{name}.sysconfig
URL:		http://www.lighttpd.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	libtool
%{?with_ssl:BuildRequires:	openssl-devel}
BuildRequires:	pcre-devel
BuildRequires:	rpmbuild(macros) >= 1.159
BuildRequires:	zlib-devel
%if %{with xattr}
BuildRequires:	attr-devel
%endif
%{?with_ldap:BuildRequires:	openldap-devel}
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_valgrind:BuildRequires:	valgrind}
PreReq:		rc-scripts
Requires(pre):	sh-utils
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Provides:	group(lighttpd)
Provides:	httpd
Provides:	user(lighttpd)
Provides:	webserver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir		%{_prefix}/%{_lib}/%{name}
%define		_lighttpddir	/home/services/%{name}
%define		_sysconfdir	/etc/%{name}

%description
lighttpd is a secure, fast, compliant and very flexible web-server
which has been optimized for high-performance environments. It has
a very low memory footprint compared to other webservers and takes
care of cpu-load. Its advanced feature-set (FastCGI, CGI, Auth,
Output-Compression, URL-Rewriting and many more) make lighttpd the
perfect webserver-software for every server that is suffering load
problems.

%description -l pl
lighttpd jest bezpiecznym, szybkim, przyjaznym i bardzo elastycznym
serwerem WWW, który zosta³ zoptymalizowany pod k±tem
wysokowydajno¶ciowych ¶rodowisk. Zajmuje bardzo ma³± ilo¶æ pamiêci
w porównaniu do innych serwerów WWW oraz dba o zajêto¶æ procesora.
Szeroki zestaw opcji (FastCGI, CGI, uwierzytelnianie, kompresja
wyj¶cia, przepisywanie URL-i i wiele innych) czyni± z lighttpd
doskona³e oprogramowanie web-serwerowe na ka¿dy serwer cierpi±cy
z powodu problemów z obci±¿eniem.

%package -n spawn-fcgi
Summary:	Spawn fcgi-process directly
Summary(pl):	Bezpo¶rednie uruchamianie procesów fcgi
Group:		Applications

%description -n spawn-fcgi
spawn-fcgi is used to spawn fcgi-process directly without the help of
a webserver or the programm itself.

%description -n spawn-fcgi -l pl
spawn-fcgi s³u¿y do uruchamiania procesów fcgi bezpo¶rednio, bez
pomocy serwera WWW ani samego programu.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%configure \
	%{?with_valgrind:--with-valgrind} \
	%{?with_xattr:--with-attr} \
	%{?with_mysql:--with-mysql} \
	%{?with_ldap:--with-ldap} \
	%{!?with_ipv6:--disable-ipv6} \
	%{!?with_largefile:--disable-lfs} \
	%{?with_ssl:--with-openssl}
	
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_lighttpddir}/{cgi-bin,html},/etc/{logrotate.d,rc.d/init.d,sysconfig},%{_sysconfdir}} \
	$RPM_BUILD_ROOT/var/log/{%{name},archiv/%{name}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE4} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}
install %{SOURCE5} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# could use automake patch, but automake generation fails...
mv $RPM_BUILD_ROOT%{_bindir}/spawn-fcgi $RPM_BUILD_ROOT%{_sbindir}/spawn-fcgi

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`/usr/bin/getgid lighttpd`" ]; then
	if [ "`/usr/bin/getgid lighttpd`" != 109 ]; then
		echo "Error: group lighttpd doesn't have gid=109. Correct this before installing %{name}." 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -g 109 lighttpd
fi
if [ -n "`/bin/id -u lighttpd 2>/dev/null`" ]; then
	if [ "`/bin/id -u lighttpd`" != 116 ]; then
		echo "Error: user lighttpd doesn't have uid=116. Correct this before installing %{name}." 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -u 116 -d %{_lighttpddir} -s /bin/false \
		-c "HTTP User" -g lighttpd lighttpd 1>&2
fi

%post
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/%{name} start\" to start %{name} daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/%{name} ]; then
		/etc/rc.d/init.d/%{name} stop 1>&2
	fi
	/sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" = "0" ]; then
	%userremove lighttpd
	%groupremove lighttpd
fi

%triggerpostun -- %{name} <= 1.3.6-2
# upgraded
if [ "$1" = "2" ]; then
%banner %{name} -e <<EOF
spawn-fcgi program is now available separately from spawn-fcgi package.

EOF
fi

%files
%defattr(644,root,root,755)
%doc NEWS README ChangeLog doc/lighttpd.conf doc/*.txt doc/rrdtool-graph.sh
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}
%attr(755,root,root) %{_libdir}/*.so
%attr(750,root,root) %dir /var/log/archiv/%{name}
%dir %attr(750,lighttpd,root) /var/log/%{name}
%attr(755,lighttpd,lighttpd) %{_lighttpddir}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/*
%dir %attr(750,root,lighttpd) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}.conf
%attr(640,root,lighttpd) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*.user
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/logrotate.d/%{name}
%{_mandir}/man?/*

%files -n spawn-fcgi
%defattr(644,root,root,755)
%doc doc/spawn-php.sh
%attr(755,root,root) %{_sbindir}/spawn-fcgi
