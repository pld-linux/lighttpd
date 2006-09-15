# TODO:
# - test ldap and mysql (failed at this time)
# - mysql issue: http://www.freebsd.org/cgi/query-pr.cgi?pr=76866
# - fam over gamin is possible, just configure doesn't check other than gamin
# - feature stat-cache-fam (doesn't work)
# - lighttpd writes early startup messages to stderr, and if started from
#   rc-scripts the stderr is closed which causes lighttpd to abort():
#   2006-07-20 21:05:52: (server.c.1233) WARNING: unknown config-key: url.rewrite-final (ignored)
#
# NOTES:
# - fcgi-devel is only used for the test-scripts
# - disable largefile, if you have 2.4 kernel to get sendfile() support, and don't need > 2GB file requests,
#   see http://article.gmane.org/gmane.comp.web.lighttpd:722
#
# Conditional build for lighttpd:
%bcond_without	xattr		# support of extended attributes
%bcond_without	ipv6		# IPv4-only version (doesn't require IPv6 in kernel)
%bcond_without	largefile	# largefile support (see notes above)
%bcond_without	ssl		# ssl support
%bcond_without	mysql		# mysql support in mod_mysql_vhost
%bcond_with	ldap		# ldap support in mod_auth
%bcond_without	lua		# LUA support in mod_cml (needs LUA >= 5.1)
%bcond_with	memcache	# memcached support in mod_cml / mod_trigger_b4_dl
%bcond_with	gamin		# gamin for reducing number of stat() calls.
				# NOTE: must be enabled in config: server.stat-cache-engine = "fam"
%bcond_with	gdbm		# gdbm in mod_trigger_b4_dl
%bcond_with	webdav_props	# properties in mod_webdav (includes extra sqlite3/libxml deps)
%bcond_with	valgrind	# compile code with valgrind support.
%bcond_with	deflate		# build deflate module (needs patch update with current svn)

# SVN snapshot
#define		_svn	1277
# Prerelease
%define _snap r1309

%define		_rel 0.59
Summary:	Fast and light HTTP server
Summary(pl):	Szybki i lekki serwer HTTP
Name:		lighttpd
Version:	1.4.12
Release:	%{_rel}%{?_snap:.%(echo %{_snap}|tr - _)}%{?_svn:.%{_svn}}
License:	BSD
Group:		Networking/Daemons
Source0:	http://www.lighttpd.net/download/%{name}-%{version}-%{_snap}.tar.gz
# Source0-md5:	a887b075858cb28bf9fd11d86556509e
Source1:	%{name}.init
Source2:	%{name}.conf
Source3:	%{name}.user
Source4:	%{name}.logrotate
Source5:	%{name}.sysconfig
Source6:	%{name}-mime.types.sh
Source7:	http://www.lighttpd.net/favicon.ico
# Source7-md5:	a358994becabd4060393a5454bde505d
Source8:	http://www.lighttpd.net/light_button.png
# Source8-md5:	02330e2313fadc29144edfd6000879f8
Source9:	http://www.lighttpd.net/light_logo.png
# Source9-md5:	ac20784510e420d5cbe5fc1cdb53d7a7
Source10:	http://gdl.hopto.org/~spider/pldstats/gfx/pld1.png
# Source10-md5:	486ecec3f6f4fe7f9bf7cee757b864f4
Source11:	%{name}-pld.html
Source100:	%{name}-mod_access.conf
Source101:	%{name}-mod_accesslog.conf
Source102:	%{name}-mod_alias.conf
Source103:	%{name}-mod_auth.conf
Source104:	%{name}-mod_cgi.conf
Source105:	%{name}-mod_cml.conf
Source106:	%{name}-mod_compress.conf
Source107:	%{name}-mod_deflate.conf
Source108:	%{name}-mod_dirlisting.conf
Source109:	%{name}-mod_evasive.conf
Source110:	%{name}-mod_evhost.conf
Source111:	%{name}-mod_expire.conf
Source112:	%{name}-mod_fastcgi.conf
Source113:	%{name}-mod_flv_streaming.conf
Source114:	%{name}-mod_indexfile.conf
Source115:	%{name}-mod_proxy.conf
Source116:	%{name}-mod_redirect.conf
Source117:	%{name}-mod_rewrite.conf
Source118:	%{name}-mod_rrdtool.conf
Source119:	%{name}-mod_scgi.conf
Source120:	%{name}-mod_secdownload.conf
Source121:	%{name}-mod_setenv.conf
Source122:	%{name}-mod_simple_vhost.conf
Source123:	%{name}-mod_ssi.conf
Source124:	%{name}-mod_staticfile.conf
Source125:	%{name}-mod_status.conf
Source126:	%{name}-mod_trigger_b4_dl.conf
Source127:	%{name}-mod_userdir.conf
Source128:	%{name}-mod_usertrack.conf
Source129:	%{name}-mod_webdav.conf
Source130:	%{name}-php-spawned.conf
Source131:	%{name}-php-external.conf
Source132:	%{name}-ssl.conf
Source133:	%{name}-mod_proxy_core.conf
Source134:	%{name}-mod_mysql_vhost.conf
Patch100:	%{name}-branch.diff
Patch0:		%{name}-mod_deflate.patch
Patch1:		%{name}-use_bin_sh.patch
Patch2:		%{name}-initgroups.patch
Patch3:		http://trac.lighttpd.net/trac/attachment/ticket/444/%{name}-apr1.patch?format=txt
Patch4:		%{name}-mod_evasive-status_code.patch
Patch5:		%{name}-lua-version.patch
URL:		http://www.lighttpd.net/
%{?with_xattr:BuildRequires:	attr-devel}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bzip2-devel
%{?with_gamin:BuildRequires:	gamin-devel}
%{?with_gdbm:BuildRequires:	gdbm-devel}
%{?with_memcache:BuildRequires:	libmemcache-devel}
BuildRequires:	libtool
BuildRequires:	libuuid-devel
%{?with_webdav_props:BuildRequires:	libxml2-devel}
%{?with_lua:BuildRequires:	lua50-devel >= 5.0.2-5.1}
BuildRequires:	mailcap >= 2.1.14-4.4
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_ldap:BuildRequires:	openldap-devel}
%{?with_ssl:BuildRequires:	openssl-devel}
BuildRequires:	pcre-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.268
%{?with_webdav_props:BuildRequires:	sqlite3-devel}
%{?with_valgrind:BuildRequires:	valgrind}
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/lib/rpm/user_group.sh
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(pre):	/usr/sbin/usermod
Requires:	%{name}-mod_dirlisting
Requires:	%{name}-mod_indexfile
Requires:	%{name}-mod_staticfile
Requires:	rc-scripts
Provides:	group(http)
Provides:	group(lighttpd)
Provides:	user(lighttpd)
Provides:	webserver
# for the posttrans scriptlet, conflicts because in vserver environment rpm package is not installed.
Conflicts:	rpm < 4.4.2-0.2
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

%package mod_access
Summary:	lighttpd module for making access restrictions
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}
Provides:	webserver(access)

%description mod_access
The access module is used to deny access to files with given trailing
path names.

%package mod_accesslog
Summary:	lighttpd module to record access logs
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description mod_accesslog
CLF like by default, flexible like Apache.

%package mod_alias
Summary:	lighttpd module for making url aliasing
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}
Provides:	webserver(alias)

%description mod_alias
The alias module is used to specify a special document-root for a
given url-subset.

%package mod_auth
Summary:	lighttpd module for authentication support
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}
Provides:	webserver(auth)

%description mod_auth
lighttpd supportes both authentication method described by RFC 2617:
basic and digest.

%package mod_cgi
Summary:	lighttpd module for CGI handling
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}
Provides:	webserver(cgi)

%description mod_cgi
The cgi module provides a CGI-conforming interface.

CGI programs allow you to enhance the functionality of the server in a
very straight and simple way...

%package mod_cml
Summary:	lighttpd module for Cache Meta Language
Summary(pl):	Modu³ Cache Meta Language
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description mod_cml
CML is a Meta language to describe the dependencies of a page at one
side and building a page from its fragments on the other side using
LUA.

%description mod_cml -l pl
CML to metajêzyk s³u¿±cy z jednej strony do opisu zale¿no¶ci strony i
z drugiej strony do budowania strony z fragmentów przy u¿yciu LUA.

%package mod_compress
Summary:	lighttpd module for output compression
Summary(pl):	Kompresja wyj¶cia
Group:		Networking/Daemons
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

%package mod_deflate
Summary:	lighttpd module for output compression
Summary(pl):	Kompresja wyj¶cia
Group:		Networking/Daemons
URL:		http://trac.lighttpd.net/trac/wiki/Mod_Deflate
Requires:	%{name} = %{version}-%{release}

%description mod_deflate
mod_deflate can compress any output from lighttpd static or dynamic.
It doesn't support caching compressed output like mod_compress.

%package mod_dirlisting
Summary:	lighttpd module for directory listings
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description mod_dirlisting
mod_dirlisting generates HTML based directory listings with full CSS
control.

%package mod_evasive
Summary:	lighttpd evasive module
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description mod_evasive

%package mod_evhost
Summary:	lighttpd module for enhanced virtual-hosting
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description mod_evhost
mod_evhost builds the document-root based on a pattern which contains
wildcards. Those wildcards can represent parts of the submitted
hostname.

%package mod_expire
Summary:	lighttpd module for controlling the expiration of content in caches
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description mod_expire
mod_expire controls the setting of the the Expire response header.

%package mod_fastcgi
Summary:	lighttpd module for FastCGI interface
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description mod_fastcgi
The FastCGI interface is the fastest and most secure way to interface
external process-handlers like Perl, PHP and your self-written
applications.

%package mod_flv_streaming
Summary:	lighttpd module for flv streaming
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description mod_flv_streaming
lighttpd module for flv streaming.

%package mod_indexfile
Summary:	lighttpd indexfile module
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}
Provides:	webserver(indexfile)

%description mod_indexfile
indexfile module.

%package mod_mysql_vhost
Summary:	lighttpd module for MySQL based vhosting
Summary(pl):	vhosty oparte na MySQL-u
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}
Conflicts:	%{name}-mod_simple_vhost

%description mod_mysql_vhost
This module provides virtual hosts (vhosts) based on a MySQL table.

%description mod_mysql_vhost -l pl
Ten modu³ udostêpnia wirtualne hosty (vhosty) oparte na tabeli MySQL.

%package mod_proxy
Summary:	lighttpd module for proxying requests
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description mod_proxy
The proxy module a simplest way to connect lighttpd to java servers
which have a HTTP-interface.

%package mod_proxy_core
Summary:	lighttpd module for proxying requests
Group:		Networking/Daemons
URL:		http://blog.lighttpd.net/articles/2006/07/18/mod_proxy_core-commited-to-svn
Requires:	%{name} = %{version}-%{release}

%description mod_proxy_core
The proxy module a simplest way to connect lighttpd to java servers
which have a HTTP-interface.

This is the new proxy code.

%package mod_redirect
Summary:	lighttpd module for URL redirects
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description mod_redirect
With mod_redirect module you can redirects a set of URLs externally.

%package mod_rewrite
Summary:	lighttpd module for internal redirects, URL rewrite
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description mod_rewrite
This module allows you rewrite a set of URLs interally in the
webserver BEFORE they are handled.

%package mod_rrdtool
Summary:	lighttpd module for monitoring traffic and server load
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}
Requires:	rrdtool

%description mod_rrdtool
RRD is a system to store and display time-series data (i.e. network
bandwidth, machine-room temperature, server load average).

With this module you can monitor the traffic and load on the
webserver.

%package mod_scgi
Summary:	lighttpd module for SCGI interface
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description mod_scgi
SCGI is a fast and simplified CGI interface. It is mostly used by
Python + WSGI.

%package mod_secdownload
Summary:	lighttpd module for secure and fast downloading
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description mod_secdownload
With this module you can easily achieve authenticated file requests
and a countermeasure against deep-linking.

%package mod_setenv
Summary:	lighttpd module for setting conditional request headers
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description mod_setenv
mod_setenv is used to add request headers.

%package mod_simple_vhost
Summary:	lighttpd module for simple virtual-hosting
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}
Conflicts:	%{name}-mod_mysql_vhost

%description mod_simple_vhost
lighttpd module for simple virtual-hosting.

%package mod_ssi
Summary:	lighttpd module for server-side includes
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description mod_ssi
The module for server-side includes provides a compatability layer for
NSCA/Apache SSI.

%package mod_staticfile
Summary:	lighttpd module for static file serving
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description mod_staticfile
lighttpd module for static file serving.

%package mod_status
Summary:	lighttpd module for displaying server status
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description mod_status
mod_status displays the server's status and configuration.

%package mod_trigger_b4_dl
Summary:	Trigger before Download
Summary(pl):	Wyzwalacz przed ¶ci±ganiem
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description mod_trigger_b4_dl
Another anti hot-linking module.

%description mod_trigger_b4_dl -l pl
Jeszcze jeden modu³ blokuj±cy bezpo¶rednie linkowanie.

%package mod_userdir
Summary:	lighttpd module for user homedirs
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description mod_userdir
The userdir module provides a simple way to link user-based
directories into the global namespace of the webserver.

%package mod_usertrack
Summary:	lighttpd usertrack module
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description mod_usertrack

%package mod_webdav
Summary:	WebDAV module for lighttpd
Summary(pl):	Modu³ WebDAV dla libghttpd
Group:		Networking/Daemons
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

%package php-spawned
Summary:	PHP support via FastCGI, spawned by lighttpd
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-mod_fastcgi = %{version}-%{release}
Requires:	php-fcgi
Obsoletes:	lighttpd-php-external

%description php-spawned
PHP support via FastCGI, spawned by lighttpd

%package php-external
Summary:	PHP support via FastCGI, spawning controlled externally
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-mod_fastcgi = %{version}-%{release}
Requires:	php-fcgi-init
Obsoletes:	lighttpd-php-spawned

%description php-external
PHP support via FastCGI, spawning controlled externally

%package ssl
Summary:	lighttpd support for SSLv2 and SSLv3
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description ssl
lighttpd support for SSLv2 and SSLv3.

%prep
%setup -q
#%patch100 -p1
#%patch0 -p1 # applied already?
#%patch1 -p1 # outdated
%patch2 -p1
#%patch3 -p1
%patch4 -p0
%patch5 -p1

# build mime.types.conf
sh %{SOURCE6} /etc/mime.types

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
install -d $RPM_BUILD_ROOT{%{_lighttpddir}/{cgi-bin,html},/etc/{logrotate.d,rc.d/init.d,sysconfig}} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{conf,webapps}.d \
	$RPM_BUILD_ROOT{/var/log/{%{name},archiv/%{name}},/var/run/%{name}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} %{SOURCE3} mime.types.conf $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE4} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}
install %{SOURCE5} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# could use automake patch, but automake generation fails...
mv $RPM_BUILD_ROOT%{_bindir}/spawn-fcgi $RPM_BUILD_ROOT%{_sbindir}/spawn-fcgi

# Install lighttpd images
install %{SOURCE7} %{SOURCE8} %{SOURCE9} $RPM_BUILD_ROOT%{_lighttpddir}/html
install %{SOURCE10} $RPM_BUILD_ROOT%{_lighttpddir}/html/pld_button.png
install %{SOURCE11} $RPM_BUILD_ROOT%{_lighttpddir}/html/index.html

# NOTE: the order of the modules is somewhat important as the modules are
# handled in the way they are specified. mod_rewrite should always be the first
# module, mod_accesslog always the last.

install %{SOURCE117} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/10_mod_rewrite.conf
install %{SOURCE116} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/11_mod_redirect.conf

install %{SOURCE100} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_access.conf
install %{SOURCE102} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_alias.conf
install %{SOURCE103} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_auth.conf
install %{SOURCE104} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_cgi.conf
install %{SOURCE105} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_cml.conf
install %{SOURCE106} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_compress.conf
install %{SOURCE107} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_deflate.conf
install %{SOURCE108} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_dirlisting.conf
install %{SOURCE109} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_evasive.conf
install %{SOURCE110} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_evhost.conf
install %{SOURCE111} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_expire.conf
install %{SOURCE112} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_fastcgi.conf
install %{SOURCE113} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_flv_streaming.conf
install %{SOURCE114} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_indexfile.conf
install %{SOURCE115} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_proxy.conf
install %{SOURCE118} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_rrdtool.conf
install %{SOURCE119} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_scgi.conf
install %{SOURCE120} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_secdownload.conf
install %{SOURCE121} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_setenv.conf
install %{SOURCE122} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_simple_vhost.conf
install %{SOURCE123} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_ssi.conf
install %{SOURCE124} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_staticfile.conf
install %{SOURCE125} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_status.conf
install %{SOURCE126} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_trigger_b4_dl.conf
install %{SOURCE127} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_userdir.conf
install %{SOURCE128} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_usertrack.conf
install %{SOURCE129} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_webdav.conf
install %{SOURCE133} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_proxy_core.conf
install %{SOURCE134} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_mysql_vhost.conf

install %{SOURCE101} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_mod_accesslog.conf

install %{SOURCE130} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/php-spawned.conf
install %{SOURCE131} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/php-external.conf
install %{SOURCE132} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/ssl.conf

%if %{without mysql}
# avoid packaging dummy module
rm -f $RPM_BUILD_ROOT%{_libdir}/mod_mysql_vhost.so
rm -f $RPM_BUILD_ROOT%{_libdir}/mod_sql_vhost_core.so
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/*_mod_mysql_vhost.conf
%endif
%if %{without deflate}
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/*_mod_deflate.conf
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 109 lighttpd
%groupadd -g 51 http
%useradd -u 116 -d %{_lighttpddir} -c "LigHTTPd User" -g lighttpd lighttpd
%addusertogroup lighttpd http

%post
/sbin/chkconfig --add %{name}

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" = "0" ]; then
	%userremove lighttpd
	%groupremove lighttpd
	%groupremove http
fi

%posttrans
# minimizing lighttpd restarts logics. we restart webserver:
#
# 1. at the end of transaction. (posttrans, feature from rpm 4.4.2)
# 2. first install of module (post: $1 = 1)
# 2. uninstall of module (postun: $1 == 0)
#
# the strict internal deps between lighttpd modules and
# main package are very important for all this to work.
%service %{name} restart "LigHTTPd webserver"
exit 0

# macro called at module post scriptlet
%define	module_post \
if [ "$1" = "1" ]; then \
	%service -q lighttpd restart \
fi

# macro called at module postun scriptlet
%define	module_postun \
if [ "$1" = "0" ]; then \
	%service -q lighttpd restart \
fi

# it's sooo annoying to write them
%define	module_scripts() \
%post %1 \
%module_post \
\
%postun %1 \
%module_postun

%module_scripts mod_access
%module_scripts mod_accesslog
%module_scripts mod_alias
%module_scripts mod_auth
%module_scripts mod_cgi
%module_scripts mod_cml
%module_scripts mod_compress
%module_scripts mod_deflate
%module_scripts mod_dirlisting
%module_scripts mod_evasive
%module_scripts mod_evhost
%module_scripts mod_expire
%module_scripts mod_fastcgi
%module_scripts mod_flv_streaming
%module_scripts mod_indexfile
%module_scripts mod_mysql_vhost
%module_scripts mod_proxy
%module_scripts mod_redirect
%module_scripts mod_rewrite
%module_scripts mod_rrdtool
%module_scripts mod_scgi
%module_scripts mod_secdownload
%module_scripts mod_setenv
%module_scripts mod_simple_vhost
%module_scripts mod_ssi
%module_scripts mod_staticfile
%module_scripts mod_status
%module_scripts mod_trigger_b4_dl
%module_scripts mod_userdir
%module_scripts mod_usertrack
%module_scripts mod_webdav

%module_scripts php-spawned
%module_scripts php-external

%triggerpostun -- %{name} <= 1.3.6-2
%banner %{name} -e <<EOF
spawn-fcgi program is now available separately from spawn-fcgi package.

EOF

%files
%defattr(644,root,root,755)
%doc NEWS README ChangeLog doc/lighttpd.conf doc/*.txt doc/rrdtool-graph.sh
%dir %attr(750,root,lighttpd) %{_sysconfdir}
%dir %attr(750,root,root) %{_sysconfdir}/webapps.d
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mime.types.conf
%attr(640,root,lighttpd) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.user

%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%attr(750,root,root) %dir /var/log/archiv/%{name}
%dir %attr(770,root,lighttpd) /var/log/%{name}
%dir %attr(770,root,lighttpd) /var/run/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/*
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}
%{_mandir}/man?/*
%dir %{_lighttpddir}
%dir %{_lighttpddir}/cgi-bin
%dir %{_lighttpddir}/html
%config(noreplace,missingok) %verify(not md5 mtime size) %{_lighttpddir}/html/*

%files mod_access
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_access.conf
%attr(755,root,root) %{_libdir}/mod_access.so

%files mod_accesslog
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_accesslog.conf
%attr(755,root,root) %{_libdir}/mod_accesslog.so

%files mod_alias
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_alias.conf
%attr(755,root,root) %{_libdir}/mod_alias.so

%files mod_auth
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_auth.conf
%attr(755,root,root) %{_libdir}/mod_auth.so

%files mod_cgi
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_cgi.conf
%attr(755,root,root) %{_libdir}/mod_cgi.so

%files mod_cml
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_cml.conf
%attr(755,root,root) %{_libdir}/mod_cml.so

%files mod_compress
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_compress.conf
%attr(755,root,root) %{_libdir}/mod_compress.so

%if %{with deflate}
%files mod_deflate
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_deflate.conf
%attr(755,root,root) %{_libdir}/mod_deflate.so
%endif

%files mod_dirlisting
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_dirlisting.conf
%attr(755,root,root) %{_libdir}/mod_dirlisting.so

%files mod_evasive
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_evasive.conf
%attr(755,root,root) %{_libdir}/mod_evasive.so

%files mod_evhost
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_evhost.conf
%attr(755,root,root) %{_libdir}/mod_evhost.so

%files mod_expire
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_expire.conf
%attr(755,root,root) %{_libdir}/mod_expire.so

%files mod_fastcgi
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_fastcgi.conf
%attr(755,root,root) %{_libdir}/mod_fastcgi.so

%files mod_flv_streaming
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_flv_streaming.conf
%attr(755,root,root) %{_libdir}/mod_flv_streaming.so

%files mod_indexfile
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_indexfile.conf
%attr(755,root,root) %{_libdir}/mod_indexfile.so

%if %{with mysql}
%files mod_mysql_vhost
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_mysql_vhost.conf
#%attr(755,root,root) %{_libdir}/mod_sql_vhost_core.so
%attr(755,root,root) %{_libdir}/mod_mysql_vhost.so
%endif

%files mod_proxy
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_proxy.conf
%attr(755,root,root) %{_libdir}/mod_proxy.so

%if 0
%files mod_proxy_core
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_proxy_core.conf
%attr(755,root,root) %{_libdir}/mod_proxy_core.so
%endif

%files mod_redirect
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_redirect.conf
%attr(755,root,root) %{_libdir}/mod_redirect.so

%files mod_rewrite
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_rewrite.conf
%attr(755,root,root) %{_libdir}/mod_rewrite.so

%files mod_rrdtool
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_rrdtool.conf
%attr(755,root,root) %{_libdir}/mod_rrdtool.so

%files mod_scgi
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_scgi.conf
%attr(755,root,root) %{_libdir}/mod_scgi.so

%files mod_secdownload
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_secdownload.conf
%attr(755,root,root) %{_libdir}/mod_secdownload.so

%files mod_setenv
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_setenv.conf
%attr(755,root,root) %{_libdir}/mod_setenv.so

%files mod_simple_vhost
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_simple_vhost.conf
%attr(755,root,root) %{_libdir}/mod_simple_vhost.so

%files mod_ssi
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_ssi.conf
%attr(755,root,root) %{_libdir}/mod_ssi.so

%files mod_staticfile
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_staticfile.conf
%attr(755,root,root) %{_libdir}/mod_staticfile.so

%files mod_status
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_status.conf
%attr(755,root,root) %{_libdir}/mod_status.so

%files mod_trigger_b4_dl
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_trigger_b4_dl.conf
%attr(755,root,root) %{_libdir}/mod_trigger_b4_dl.so

%files mod_userdir
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_userdir.conf
%attr(755,root,root) %{_libdir}/mod_userdir.so

%files mod_usertrack
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_usertrack.conf
%attr(755,root,root) %{_libdir}/mod_usertrack.so

%files mod_webdav
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_webdav.conf
%attr(755,root,root) %{_libdir}/mod_webdav.so

%files -n spawn-fcgi
%defattr(644,root,root,755)
%doc doc/spawn-php.sh
%attr(755,root,root) %{_sbindir}/spawn-fcgi

%files php-spawned
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/php-spawned.conf

%files php-external
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/php-external.conf

%files ssl
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/ssl.conf
