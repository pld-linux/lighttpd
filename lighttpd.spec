# TODO:
# - test ldap and mysql (failed at this time)
# - mysql issue: http://www.freebsd.org/cgi/query-pr.cgi?pr=76866
# - fam over gamin is possible, just configure doesn't check other than gamin
# - lua50 isn't properly detected
#
# NOTES:
# - fcgi-devel is only used for the test-scripts
# - disable largefile, if you have 2.4 kernel to get sendfile() support, and don't need > 2GB file requests,
#   see http://article.gmane.org/gmane.comp.web.lighttpd:722
# - please make subpackages of modules that depend other modules than:
#  - pcre (core binary needs it too)
#  - openssl (core binary needs it too)
#
# Conditional build for lighttpd:
%bcond_without	xattr			# support of extended attributes
%bcond_without	ipv6			# IPv4-only version (doesn't require IPv6 in kernel)
%bcond_without	largefile		# largefile support (see notes above)
%bcond_without	ssl				# ssl support
%bcond_with		mysql			# mysql support in mod_mysql_vhost
%bcond_with		ldap			# ldap support in mod_auth
%bcond_with		lua				# LUA support in mod_cml
%bcond_with		memcache		# memcached support in mod_cml / mod_trigger_b4_dl
%bcond_with		gamin			# gamin for reducing number of stat() calls. NOTE: must be enabled in config: server.stat-cache-engine = "fam"
%bcond_with		gdbm			# gdbm in mod_trigger_b4_dl
%bcond_with		webdav_props	# properties in mod_webdav (includes extra sqlite3/libxml deps)
%bcond_with		valgrind		# compile code with valgrind support.
%bcond_with		dirhide			# with 'hide from dirlisting' hack

# Prerelease snapshot: DATE-TIME
#define _snap 20050116-1743

%if 0%{?_snap}
%define _source http://www.lighttpd.net/download/%{name}-%{version}-%{_snap}.tar.gz
%else
%define _source http://www.lighttpd.net/download/%{name}-%{version}.tar.gz
%endif

%define		_rel 0.4

Summary:	Fast and light HTTP server
Summary(pl):	Szybki i lekki serwer HTTP
Name:		lighttpd
Version:	1.4.1
Release:	%{_rel}%{?_snap:.%(echo %{_snap}|tr - _)}
Group:		Networking/Daemons
License:	BSD
Source0:	%{_source}
# Source0-md5:	3abffbe574fd835721760a37c00d3714
Source1:	%{name}.init
Source2:	%{name}.conf
Source3:	%{name}.user
Source4:	%{name}.logrotate
Source5:	%{name}.sysconfig
Patch0:		http://minghetti.ch/blob/dirlist-hide.patch
Patch1:		%{name}-fcgi-verbose.patch
Patch2:		%{name}-ssl-redirect-fix.patch
Patch3:		%{name}-lua-pkgconfig.patch
Patch4:	%{name}-openssl.patch
URL:		http://www.lighttpd.net/
%{?with_xattr:BuildRequires:	attr-devel}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bzip2-devel
%{?with_gamin:BuildRequires:	gamin-devel}
%{?with_webdav_props:BuildRequires:	sqlite3-devel}
%{?with_webdav_props:BuildRequires:	libxml2-devel}
BuildRequires:	libtool
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_ldap:BuildRequires:		openldap-devel}
%{?with_ssl:BuildRequires:	openssl-devel}
%{?with_lua:BuildRequires:	lua50-devel >= 5.0.2-4.1}
%{?with_memcache:BuildRequires:	libmemcache-devel}
%{?with_gdbm:BuildRequires:	gdbm-devel}
BuildRequires:	pcre-devel
BuildRequires:	rpmbuild(macros) >= 1.202
%{?debug:BuildRequires:	valgrind}
BuildRequires:	zlib-devel
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
which has been optimized for high-performance environments. It has a
very low memory footprint compared to other webservers and takes care
of cpu-load. Its advanced feature-set (FastCGI, CGI, Auth,
Output-Compression, URL-Rewriting and many more) make lighttpd the
perfect webserver-software for every server that is suffering load
problems.

%description -l pl
lighttpd jest bezpiecznym, szybkim, przyjaznym i bardzo elastycznym
serwerem WWW, który zosta³ zoptymalizowany pod k±tem
wysokowydajno¶ciowych ¶rodowisk. Zajmuje bardzo ma³± ilo¶æ pamiêci w
porównaniu do innych serwerów WWW oraz dba o zajêto¶æ procesora.
Szeroki zestaw opcji (FastCGI, CGI, uwierzytelnianie, kompresja
wyj¶cia, przepisywanie URL-i i wiele innych) czyni± z lighttpd
doskona³e oprogramowanie web-serwerowe na ka¿dy serwer cierpi±cy z
powodu problemów z obci±¿eniem.

%package mod_compress
Summary:	Output Compression
Summary(pl):	Kompresja wyj¶cia
Group:		Networking/Daemons
URL:		http://www.lighttpd.net/documentation/compress.html
Requires:	%{name} = %{version}-%{release}

%description mod_compress
Output compression reduces the network load and can improve the
overall throughput of the webserver.

Only static content is supported up to now.

The server negotiates automatically which compression method is used.
Supported are gzip, deflate, bzip.

%description mod_compress -l pl
Kompresja wyj¶cia zmniejsza obci±¿enie sieci i mo¿e poprawiæ ca³kowit±
przepustowo¶æ serwera WWW.

Jak na razie obs³ugiwana jest tylko statyczna tre¶æ.

Serwer automatycznie negocjuje, która metoda kompresji jest u¿ywana.
Obs³ugiwane s± gzip, deflate i bzip.

%package mod_cml
Summary:	Cache Meta Language module
Summary(pl):	Modu³ Cache Meta Language
Group:		Networking/Daemons
URL:		http://www.lighttpd.net/documentation/cml.html
Requires:	%{name} = %{version}-%{release}

%description mod_cml
CML is a Meta language to describe the dependencies of a page at one
side and building a page from its fragments on the other side using
LUA.

%description mod_cml -l pl
CML to metajêzyk s³u¿±cy z jednej strony do opisu zale¿no¶ci strony i
z drugiej strony do budowania strony z fragmentów przy u¿yciu LUA.

%package mod_mysql_vhost
Summary:	MySQL based vhosting
Summary(pl):	vhosty oparte na MySQL-u
Group:		Networking/Daemons
URL:		http://www.lighttpd.net/documentation/mysqlvhost.html
Requires:	%{name} = %{version}-%{release}

%description mod_mysql_vhost
This module provides virtual hosts (vhosts) based on a MySQL table.

%description mod_mysql_vhost -l pl
Ten modu³ udostêpnia wirtualne hosty (vhosty) oparte na tabeli MySQL.

%package mod_trigger_b4_dl
Summary:	Trigger before Download
Summary(pl):	Wyzwalacz przed ¶ci±ganiem
Group:		Networking/Daemons
URL:		http://www.lighttpd.net/documentation/trigger_b4_dl.html
Requires:	%{name} = %{version}-%{release}

%description mod_trigger_b4_dl
Another anti hot-linking module.

%description mod_trigger_b4_dl -l pl
Jeszcze jeden modu³ blokuj±cy bezpo¶rednie linkowanie.

%package mod_webdav
Summary:	WebDAV module for lighttpd
Summary(pl):	Modu³ WebDAV dla libghttpd
Group:		Networking/Daemons
URL:		http://www.lighttpd.net/documentation/webdav.html
Requires:	%{name} = %{version}-%{release}

%description mod_webdav
The WebDAV module is a very minimalistic implementation of RFC 2518.
Minimalistic means that not all operations are implementated yet.

So far we have
- PROPFIND
- OPTIONS
- MKCOL
- DELETE
- PUT

and the usual GET, POST, HEAD from HTTP/1.1.

So far mounting a webdav resource into Windows XP works and the basic
litmus tests are passed.

%description mod_webdav -l pl
Modu³ WebDAV to bardzo minimalistyczna implementacja RFC 2518.
Minimalistyczna oznacza, ¿e jeszcze nie wszystkie operacje s±
zaimplementowane. Jak na razie s±:
- PROPFIND
- OPTIONS
- MKCOL
- DELETE
- PUT
oraz zwyk³e GET, POST, HEAD z HTTP/1.1.

Jak na razie montowanie zasobu webdav pod Windows XP dzia³a i
podstawowe testy lakmusowe przechodz±.

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
%{?with_dirhide:%patch0 -p0}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p2

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}

%configure \
	%{!?with_ipv6:--disable-ipv6} \
	%{!?with_largefile:--disable-lfs} \
	%{?with_valgrind:--with-valgrind} \
	%{?with_xattr:--with-attr} \
	%{?with_mysql:--with-mysql} \
	%{?with_ldap:--with-ldap} \
	%{?with_ssl:--with-openssl} \
	%{?with_lua:--with-lua} \
	%{?with_memcache:--with-memcache} \
	%{?with_webdav_props:--with-webdav-props} \
	%{?with_gamin:--with-gamin} \
	%{?with_gdbm:--with-gdbm}

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
%groupadd -g 109 lighttpd
%useradd -u 116 -d %{_lighttpddir} -c "HTTP User" -g lighttpd lighttpd

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
%attr(755,root,root) %{_libdir}/mod_access.so
%attr(755,root,root) %{_libdir}/mod_accesslog.so
%attr(755,root,root) %{_libdir}/mod_alias.so
%attr(755,root,root) %{_libdir}/mod_auth.so
%attr(755,root,root) %{_libdir}/mod_cgi.so
%attr(755,root,root) %{_libdir}/mod_dirlisting.so
%attr(755,root,root) %{_libdir}/mod_evhost.so
%attr(755,root,root) %{_libdir}/mod_expire.so
%attr(755,root,root) %{_libdir}/mod_fastcgi.so
%attr(755,root,root) %{_libdir}/mod_indexfile.so
%attr(755,root,root) %{_libdir}/mod_proxy.so
%attr(755,root,root) %{_libdir}/mod_redirect.so
%attr(755,root,root) %{_libdir}/mod_rewrite.so
%attr(755,root,root) %{_libdir}/mod_rrdtool.so
%attr(755,root,root) %{_libdir}/mod_scgi.so
%attr(755,root,root) %{_libdir}/mod_secdownload.so
%attr(755,root,root) %{_libdir}/mod_setenv.so
%attr(755,root,root) %{_libdir}/mod_simple_vhost.so
%attr(755,root,root) %{_libdir}/mod_ssi.so
%attr(755,root,root) %{_libdir}/mod_staticfile.so
%attr(755,root,root) %{_libdir}/mod_status.so
%attr(755,root,root) %{_libdir}/mod_userdir.so
%attr(755,root,root) %{_libdir}/mod_usertrack.so
%attr(750,root,root) %dir /var/log/archiv/%{name}
%dir %attr(750,lighttpd,root) /var/log/%{name}
%attr(755,lighttpd,lighttpd) %{_lighttpddir}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/*
%dir %attr(750,root,lighttpd) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%attr(640,root,lighttpd) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.user
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%{_mandir}/man?/*

%files mod_compress
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/mod_compress.so

%files mod_cml
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/mod_cml.so

%if %{with mysql}
%files mod_mysql_vhost
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/mod_mysql_vhost.so
%endif

%files mod_trigger_b4_dl
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/mod_trigger_b4_dl.so

%files mod_webdav
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/mod_webdav.so

%files -n spawn-fcgi
%defattr(644,root,root,755)
%doc doc/spawn-php.sh
%attr(755,root,root) %{_sbindir}/spawn-fcgi
