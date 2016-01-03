
# TODO:
# - provide or autogenerate self signed cert in post, so after installing
#   lighttpd-ssl server will still work
# - patch with mod_websocket: https://github.com/Juniper/lighttpd-for-juise
#
# Conditional build:
%bcond_with		tests		# build with tests
%bcond_without	xattr		# support of extended attributes
%bcond_without	ipv6		# IPv4-only version (doesn't require IPv6 in kernel)
%bcond_without	largefile	# largefile support (see notes above)
%bcond_without	ssl		# ssl support
%bcond_without	mysql		# mysql support in mod_mysql_vhost
%bcond_without	ldap		# ldap support in mod_auth
%bcond_without	lua		# LUA support in mod_cml (needs LUA >= 5.1)
%bcond_with	memcache	# memcached support in mod_cml / mod_trigger_b4_dl
%bcond_with	gamin		# gamin for reducing number of stat() calls.
				# NOTE:	must be enabled in config: server.stat-cache-engine = "fam"
%bcond_with	gdbm		# gdbm in mod_trigger_b4_dl
%bcond_with	webdav_props	# properties in mod_webdav (includes extra sqlite3/libxml deps)
%bcond_with	webdav_locks	# webdav locks with extra efsprogs deps
%bcond_with	valgrind	# compile code with valgrind support.
%bcond_with	deflate		# build deflate module (needs patch update with current svn)
%bcond_with	h264_streaming		# build h264_streaming module

%if %{with webdav_locks}
%define		webdav_progs	1
%endif

Summary:	Fast and light HTTP server
Summary(pl.UTF-8):	Szybki i lekki serwer HTTP
Name:		lighttpd
Version:	1.4.39
Release:	1
License:	BSD
Group:		Networking/Daemons/HTTP
Source0:	http://download.lighttpd.net/lighttpd/releases-1.4.x/%{name}-%{version}.tar.xz
# Source0-md5:	63c7563be1c7a7a9819a51f07f1af8b2
Source1:	%{name}.init
Source2:	%{name}.conf
Source3:	%{name}.user
Source4:	%{name}.logrotate
Source5:	%{name}.sysconfig
Source6:	%{name}-mime.types.sh
Source7:	http://glen.alkohol.ee/pld/lighty/favicon.ico
# Source7-md5:	00fcac5b861a54f5eb147a589504d480
Source8:	light_button.png
# Source8-md5:	3e1008ee1d3d6d390cf81fe3072b4f50
Source9:	light_logo.png
# Source9-md5:	cbb7f0676e51ee2e26cf004df293fc62
Source10:	pld_button.png
# Source10-md5:	185afa921e81bd726b9f0f9f0909dc6e
Source11:	%{name}-pld.html
Source12:	%{name}.monitrc
Source13:	branch.sh
Source14:	TODO
Source16:	%{name}.tmpfiles
Source17:	%{name}.service
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
Source133:	%{name}-mod_mysql_vhost.conf
Source134:	%{name}-mod_magnet.conf
Source135:	%{name}-mod_extforward.conf
Source136:	%{name}-mod_h264_streaming.conf
Source137:	%{name}-mod_cgi_php.conf
Source138:	%{name}-mod_compress.tmpwatch
# use branch.sh script to create branch.diff
#Patch100:	%{name}-branch.diff
## Patch100-md5:	cdcde8cb4632a42c5ae21d73aae9d34b
Patch0:		%{name}-use_bin_sh.patch
Patch1:		%{name}-mod_evasive-status_code.patch
Patch2:		%{name}-mod_h264_streaming.patch
Patch3:		%{name}-branding.patch
Patch5:		%{name}-mod_deflate.patch
Patch6:		test-port-setup.patch
Patch7:		env-documentroot.patch
#Patch:		%{name}-modinit-before-fork.patch
#Patch:		%{name}-errorlog-before-fork.patch
URL:		http://www.lighttpd.net/
%{?with_xattr:BuildRequires:	attr-devel}
BuildRequires:	autoconf >= 2.57
%if "%{pld_release}" != "ac"
BuildRequires:	automake >= 1:1.11.2
%else
BuildRequires:	automake
%endif
BuildRequires:	bzip2-devel
BuildRequires:	fcgi-devel
%{?with_gamin:BuildRequires:	gamin-devel}
%{?with_gdbm:BuildRequires:	gdbm-devel}
%{?with_memcache:BuildRequires:	libmemcache-devel}
BuildRequires:	libtool
BuildRequires:	libuuid-devel
%{?with_webdav_props:BuildRequires:	libxml2-devel}
%{?with_lua:BuildRequires:	lua51-devel}
BuildRequires:	mailcap >= 2.1.14-4.4
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_ldap:BuildRequires:	openldap-devel}
%{?with_ssl:BuildRequires:	openssl-devel}
BuildRequires:	pcre-devel
BuildRequires:	pkgconfig
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpmbuild(macros) >= 1.647
%{?with_webdav_props:BuildRequires:	sqlite3-devel}
BuildRequires:	tar >= 1:1.22
%{?with_valgrind:BuildRequires:	valgrind}
BuildRequires:	which
BuildRequires:	xz
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
Requires:	%{name}-mod_dirlisting = %{version}-%{release}
Requires:	%{name}-mod_indexfile = %{version}-%{release}
Requires:	%{name}-mod_staticfile = %{version}-%{release}
Requires:	rc-scripts >= 0.4.3.0
Requires:	rpm-whiteout >= 1.5
Requires:	systemd-units >= 38
Suggests:	%{name}-mod_accesslog
Provides:	group(http)
Provides:	group(lighttpd)
Provides:	user(lighttpd)
Provides:	webserver
Provides:	webserver(headers)
Provides:	webserver(mime)
Conflicts:	logrotate < 3.7-4
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

%description -l pl.UTF-8
lighttpd jest bezpiecznym, szybkim, przyjaznym i bardzo elastycznym
serwerem WWW, który został zoptymalizowany pod kątem
wysokowydajnościowych środowisk. Zajmuje bardzo małą ilość pamięci w
porównaniu do innych serwerów WWW oraz dba o zajętość procesora.
Szeroki zestaw opcji (FastCGI, CGI, uwierzytelnianie, kompresja
wyjścia, przepisywanie URL-i i wiele innych) czynią z lighttpd
doskonałe oprogramowanie web-serwerowe na każdy serwer cierpiący z
powodu problemów z obciążeniem.

%package mod_access
Summary:	lighttpd module for making access restrictions
Summary(pl.UTF-8):	Moduł lighttpd ograniczający dostęp
Group:		Networking/Daemons/HTTP
URL:		http://redmine.lighttpd.net/projects/lighttpd/wiki/Docs:ModAccess
Requires:	%{name} = %{version}-%{release}
Provides:	webserver(access)

%description mod_access
The access module is used to deny access to files with given trailing
path names.

%description mod_access -l pl.UTF-8
Moduł access służy do ograniczania dostępu do plików o podanych
ścieżkach.

%package mod_accesslog
Summary:	lighttpd module to record access logs
Summary(pl.UTF-8):	Moduł lighttpd do zapisu logów dostępu
Group:		Networking/Daemons/HTTP
URL:		http://redmine.lighttpd.net/projects/lighttpd/wiki/Docs:ModAccessLog
Requires:	%{name} = %{version}-%{release}

%description mod_accesslog
CLF like by default, flexible like Apache.

%description mod_accesslog -l pl.UTF-8
Domyślnie podobny do CLF, elastyczny jak Apache.

%package mod_alias
Summary:	lighttpd module for making URL aliasing
Summary(pl.UTF-8):	Moduł lighttpd odpowiadający za aliasy URL-i
Group:		Networking/Daemons/HTTP
URL:		http://redmine.lighttpd.net/projects/lighttpd/wiki/Docs:ModAlias
Requires:	%{name} = %{version}-%{release}
Provides:	webserver(alias)

%description mod_alias
The alias module is used to specify a special document-root for a
given URL-subset.

%description mod_alias -l pl.UTF-8
Modul alias służy do określania specjalnego drzewa (document-roota)
dla podanego podzbioru URL-i.

%package mod_auth
Summary:	lighttpd module for authentication support
Summary(pl.UTF-8):	Moduł lighttpd do obsługi uwierzytelniania
Group:		Networking/Daemons/HTTP
URL:		http://redmine.lighttpd.net/projects/lighttpd/wiki/Docs:ModAuth
Requires:	%{name} = %{version}-%{release}
Provides:	webserver(auth)

%description mod_auth
lighttpd supportes both authentication method described by RFC 2617:
basic and digest.

%description mod_auth -l pl.UTF-8
lighttpd obsługuje obie metody uwierzytelniania opisane w RFC 2617:
basic i digest.

%package mod_cgi
Summary:	lighttpd module for CGI handling
Summary(pl.UTF-8):	Moduł lighttpd do obsługi CGI
Group:		Networking/Daemons/HTTP
URL:		http://redmine.lighttpd.net/projects/lighttpd/wiki/Docs:ModCGI
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-mod_alias = %{version}-%{release}
Provides:	webserver(cgi)

%description mod_cgi
The cgi module provides a CGI-conforming interface.

CGI programs allow you to enhance the functionality of the server in a
very straight and simple way.

%description mod_cgi -l pl.UTF-8
Moduł cgi udostępnia interfejs zgodny z CGI.

Programy CGI pozwalają rozszerzać funkcjonalność serwera w bardzo
prosty i naturalny sposób.

%package mod_cgi_php
Summary:	lighttpd module for CGI handling PHP scripts
Summary(pl.UTF-8):	Moduł lighttpd do obsługi skryptów PHP przez CGI
Group:		Networking/Daemons/HTTP
Requires:	%{name}-mod_cgi = %{version}-%{release}
Requires:	php(cgi)
Provides:	webserver(php)

%description mod_cgi_php
The cgi module provides a CGI-conforming interface for PHP scripts.

CGI programs allow you to enhance the functionality of the server in a
very straight and simple way.

%description mod_cgi_php -l pl.UTF-8
Moduł cgi udostępnia interfejs zgodny z CGI do wywoływania skryptów
PHP.

Programy CGI pozwalają rozszerzać funkcjonalność serwera w bardzo
prosty i naturalny sposób.

%package mod_cml
Summary:	lighttpd module for Cache Meta Language
Summary(pl.UTF-8):	Moduł Cache Meta Language
Group:		Networking/Daemons/HTTP
URL:		http://redmine.lighttpd.net/projects/lighttpd/wiki/Docs:ModCML
Requires:	%{name} = %{version}-%{release}

%description mod_cml
CML is a Meta language to describe the dependencies of a page at one
side and building a page from its fragments on the other side using
LUA.

%description mod_cml -l pl.UTF-8
CML to metajęzyk służący z jednej strony do opisu zależności strony i
z drugiej strony do budowania strony z fragmentów przy użyciu LUA.

%package mod_compress
Summary:	lighttpd module for output compression
Summary(pl.UTF-8):	Moduł lighttpd do kompresji wyjścia
Group:		Networking/Daemons/HTTP
URL:		http://redmine.lighttpd.net/projects/lighttpd/wiki/Docs:ModCompress
Requires:	%{name} = %{version}-%{release}

%description mod_compress
Output compression reduces the network load and can improve the
overall throughput of the webserver.

Only static content is supported up to now.

The server negotiates automatically which compression method is used.
Supported are gzip, deflate, bzip.

%description mod_compress -l pl.UTF-8
Kompresja wyjścia zmniejsza obciążenie sieci i może poprawić całkowitą
przepustowość serwera WWW.

Jak na razie obsługiwana jest tylko statyczna treść.

Serwer automatycznie negocjuje, która metoda kompresji jest używana.
Obsługiwane są gzip, deflate i bzip.

%package mod_deflate
Summary:	lighttpd module for output compression using deflate method
Summary(pl.UTF-8):	Moduł lighttpd do kompresji wyjścia metodą deflate
Group:		Networking/Daemons/HTTP
URL:		http://redmine.lighttpd.net/projects/lighttpd/wiki/Mod_Deflate
Requires:	%{name} = %{version}-%{release}

%description mod_deflate
mod_deflate can compress any output from lighttpd static or dynamic.
It doesn't support caching compressed output like mod_compress.

%description mod_deflate -l pl.UTF-8
mod_deflate potrafi kompresować statyczne i dynamiczne wyjście z
lighttpd. Nie obsługuje cache'owania wyniku kompresji, jak robi to
mod_compress.

%package mod_dirlisting
Summary:	lighttpd module for directory listings
Summary(pl.UTF-8):	Moduł lighttpd do tworzenia listingów katalogów
Group:		Networking/Daemons/HTTP
URL:		http://redmine.lighttpd.net/projects/lighttpd/wiki/Docs:ModDirlisting
Requires:	%{name} = %{version}-%{release}

%description mod_dirlisting
mod_dirlisting generates HTML based directory listings with full CSS
control.

%description mod_dirlisting -l pl.UTF-8
mod_dirlisting tworzy listingi katalogów w formacie HTML z pełną
kontrolą CSS.

%package mod_evasive
Summary:	lighttpd evasive module
Summary(pl.UTF-8):	Moduł evasive dla lighttpd
Group:		Networking/Daemons/HTTP
URL:		http://redmine.lighttpd.net/projects/lighttpd/wiki/Docs:ModEvasive
Requires:	%{name} = %{version}-%{release}

%description mod_evasive
lighttpd evasive module.

%description mod_evasive -l pl.UTF-8
Moduł evasive dla lighttpd.

%package mod_evhost
Summary:	lighttpd module for enhanced virtual-hosting
Summary(pl.UTF-8):	Moduł lighttpd rozszerzający obsługę hostów wirtualnych
Group:		Networking/Daemons/HTTP
URL:		http://redmine.lighttpd.net/projects/lighttpd/wiki/Docs:ModEVhost
Requires:	%{name} = %{version}-%{release}

%description mod_evhost
mod_evhost builds the document-root based on a pattern which contains
wildcards. Those wildcards can represent parts of the submitted
hostname.

%description mod_evhost -l pl.UTF-8
mod_evhost tworzy document-root w oparciu o wzorzec zawierający znaki
wieloznaczne (wildcards). Znaki te reprezentują części przekazanej
nazwy hosta.

%package mod_expire
Summary:	lighttpd module for controlling the expiration of content in caches
Summary(pl.UTF-8):	Moduł lighttpd sterujący wygasaniem treści w cache'ach
Group:		Networking/Daemons/HTTP
URL:		http://redmine.lighttpd.net/projects/lighttpd/wiki/Docs:ModExpire
Requires:	%{name} = %{version}-%{release}
Provides:	webserver(expires)

%description mod_expire
mod_expire controls the setting of the the Expire response header.

%description mod_expire -l pl.UTF-8
mod_expire steruje ustawianiem nagłówka odpowiedzi Expire.

%package mod_extforward
Summary:	lighttpd module to extract the client's "real" IP from X-Forwarded-For header
Summary(pl.UTF-8):	Moduł lighttpd wyciągający "prawdziwy" IP klienta z nagłówka X-Forwarded-For
Group:		Networking/Daemons/HTTP
URL:		http://redmine.lighttpd.net/projects/lighttpd/wiki/DocsModExtForward
Requires:	%{name} = %{version}-%{release}

%description mod_extforward
This module will extract the client's "real" IP from X-Forwarded-For
header which is added by Squid or other proxies. It might be useful
for servers behind reverse proxy servers.

%description mod_extforward -l pl.UTF-8
Ten moduł wyciąga "prawdziwy" IP klienta z nagłówka X-Forwarded-For
dodawanego przez Squida czy inne proxy. Może być przydatny dla
serwerów stojących za odwrotnymi serwerami proxy.

%package mod_fastcgi
Summary:	lighttpd module for FastCGI interface
Summary(pl.UTF-8):	Moduł lighttpd do interfejsu FastCGI
Group:		Networking/Daemons/HTTP
URL:		http://redmine.lighttpd.net/projects/lighttpd/wiki/Docs:ModFastCGI
Requires:	%{name} = %{version}-%{release}

%description mod_fastcgi
The FastCGI interface is the fastest and most secure way to interface
external process-handlers like Perl, PHP and your self-written
applications.

%description mod_fastcgi -l pl.UTF-8
Interfejs FastCGI to najszybszy i najbezpieczniejszy sposób
komunikacji z zewnętrznymi programami obsługującymi procesy, takimi
jak Perl, PHP czy własne aplikacje.

%package mod_flv_streaming
Summary:	lighttpd module for flv streaming
Summary(pl.UTF-8):	Moduł lighttpd do streamingu flv
Group:		Networking/Daemons/HTTP
URL:		http://redmine.lighttpd.net/projects/lighttpd/wiki/Docs:ModFLVStreaming
Requires:	%{name} = %{version}-%{release}

%description mod_flv_streaming
lighttpd module for flv streaming.

%description mod_flv_streaming -l pl.UTF-8
Moduł lighttpd do streamingu flv.

%package mod_h264_streaming
Summary:	lighttpd module for h264 streaming
Summary(pl.UTF-8):	Moduł lighttpd do emisji strumieni h264
License:	CC 3.0 BY-NC-SA
Group:		Networking/Daemons/HTTP
URL:		http://h264.code-shop.com/trac/wiki/Mod-H264-Streaming-Lighttpd-Version2
Requires:	%{name} = %{version}-%{release}

%description mod_h264_streaming
A lighttpd plugin for pseudo-streaming QuickTime/MPEG-4 files.

%description mod_h264_streaming -l pl.UTF-8
Moduł lighttpd do pseudostreamingu plików QuickTime/MPEG-4.

%package mod_indexfile
Summary:	lighttpd indexfile module
Summary(pl.UTF-8):	Moduł indexfile dla lighttpd
Group:		Networking/Daemons/HTTP
URL:		http://redmine.lighttpd.net/projects/lighttpd/wiki/Index-file-names.Details
Requires:	%{name} = %{version}-%{release}
Provides:	webserver(indexfile)

%description mod_indexfile
indexfile module.

%description mod_indexfile -l pl.UTF-8
Moduł indexfile.

%package mod_magnet
Summary:	lighttpd powermagnet module
Summary(pl.UTF-8):	Moduł powermagnet dla lighttpd
Group:		Networking/Daemons/HTTP
URL:		http://redmine.lighttpd.net/wiki/lighttpd/Docs:ModMagnet
Requires:	%{name} = %{version}-%{release}

%description mod_magnet
mod_magnet is a module to control the request handling in lighty.

%description mod_magnet -l pl.UTF-8
mod_magnet to moduł sterujący obsługą żądań w lighty.

%package mod_mysql_vhost
Summary:	lighttpd module for MySQL based vhosting
Summary(pl.UTF-8):	Moduł lighttpd obsługujący vhosty oparte na MySQL-u
Group:		Networking/Daemons/HTTP
URL:		http://redmine.lighttpd.net/projects/lighttpd/wiki/Docs:ModMySQLVhost
Requires:	%{name} = %{version}-%{release}
Conflicts:	%{name}-mod_simple_vhost

%description mod_mysql_vhost
This module provides virtual hosts (vhosts) based on a MySQL table.

%description mod_mysql_vhost -l pl.UTF-8
Ten moduł udostępnia wirtualne hosty (vhosty) oparte na tabeli MySQL.

%package mod_proxy
Summary:	lighttpd module for proxying requests
Summary(pl.UTF-8):	Moduł lighttpd do przekazywania żądań
Group:		Networking/Daemons/HTTP
URL:		http://redmine.lighttpd.net/projects/lighttpd/wiki/Docs:ModProxy
Requires:	%{name} = %{version}-%{release}

%description mod_proxy
The proxy module a simplest way to connect lighttpd to Java servers
which have a HTTP-interface.

%description mod_proxy -l pl.UTF-8
Moduł proxy to najprostszy sposób łączenia lighttpd z serwerami Javy
mającymi interfejs HTTP.

%package mod_proxy_core
Summary:	lighttpd module for proxying requests
Summary(pl.UTF-8):	Moduł lighttpd do przekazywania żądań
Group:		Networking/Daemons/HTTP
URL:		http://blog.lighttpd.net/articles/2006/07/18/mod_proxy_core-commited-to-svn
Requires:	%{name} = %{version}-%{release}

%description mod_proxy_core
The proxy module a simplest way to connect lighttpd to java servers
which have a HTTP-interface.

This is the new proxy code.

%description mod_proxy_core -l pl.UTF-8
Moduł proxy to najprostszy sposób łączenia lighttpd z serwerami Javy
mającymi interfejs HTTP.

Ten pakiet zawiera nowy moduł proxy.

%package mod_redirect
Summary:	lighttpd module for URL redirects
Summary(pl.UTF-8):	Moduł lighttpd do przekierowań URL-i
Group:		Networking/Daemons/HTTP
URL:		http://redmine.lighttpd.net/projects/lighttpd/wiki/Docs:ModRedirect
Requires:	%{name} = %{version}-%{release}

%description mod_redirect
With mod_redirect module you can redirect a set of URLs externally.

%description mod_redirect -l pl.UTF-8
Przy użyciu modułu mod_redirect można przekierować zbiór URL-i na
zewnątrz.

%package mod_rewrite
Summary:	lighttpd module for internal redirects, URL rewrite
Summary(pl.UTF-8):	Moduł lighttpd do wewnętrznych przekierowań i przepisywania URL-i
Group:		Networking/Daemons/HTTP
URL:		http://redmine.lighttpd.net/projects/lighttpd/wiki/Docs:ModRewrite
Requires:	%{name} = %{version}-%{release}
Provides:	webserver(rewrite)

%description mod_rewrite
This module allows you rewrite a set of URLs interally in the
webserver BEFORE they are handled.

%description mod_rewrite -l pl.UTF-8
Ten moduł pozwala na przepisywanie zbioru URL-i wewnętrznie w serwerze
WWW _przed_ ich obsługą.

%package mod_rrdtool
Summary:	lighttpd module for monitoring traffic and server load
Summary(pl.UTF-8):	Moduł lighttpd do monitorowania ruchu i obciążenia serwera
Group:		Networking/Daemons/HTTP
URL:		http://redmine.lighttpd.net/projects/lighttpd/wiki/Docs:ModRRDTool
Requires:	%{name} = %{version}-%{release}
Requires:	rrdtool

%description mod_rrdtool
RRD is a system to store and display time-series data (i.e. network
bandwidth, machine-room temperature, server load average).

With this module you can monitor the traffic and load on the
webserver.

%description mod_rrdtool -l pl.UTF-8
RRD to system przechowywania i wyświetlania danych zależnych od czasu
(np. obciążenia sieci, temperatury w serwerowni, średniego obciążenia
serwera).

Przy użyciu tego modułu można monitorować ruch i obciążenie serwera
WWW.

%package mod_scgi
Summary:	lighttpd module for SCGI interface
Summary(pl.UTF-8):	Moduł lighttpd do interfejsu SCGI
Group:		Networking/Daemons/HTTP
URL:		http://redmine.lighttpd.net/projects/lighttpd/wiki/Docs:ModSCGI
Requires:	%{name} = %{version}-%{release}

%description mod_scgi
SCGI is a fast and simplified CGI interface. It is mostly used by
Python + WSGI.

%description mod_scgi -l pl.UTF-8
SCGI to szybki i uproszczony interfejs CGI. Jest używany głównie przez
Pythona z WSGI.

%package mod_secdownload
Summary:	lighttpd module for secure and fast downloading
Summary(pl.UTF-8):	Moduł lighttpd do bezpiecznego i szybkiego ściągania danych
Group:		Networking/Daemons/HTTP
URL:		http://redmine.lighttpd.net/projects/lighttpd/wiki/Docs:ModSecDownload
Requires:	%{name} = %{version}-%{release}

%description mod_secdownload
With this module you can easily achieve authenticated file requests
and a countermeasure against deep-linking.

%description mod_secdownload -l pl.UTF-8
Przy użyciu tego modułu można łatwo umożliwić ściąganie plików z
uwierzytelnieniem i zapobiec używaniu bezpośrednich odnośników.

%package mod_setenv
Summary:	lighttpd module for setting conditional request headers
Summary(pl.UTF-8):	Moduł lighttpd do ustawiania warunkowych nagłówków żądań
Group:		Networking/Daemons/HTTP
URL:		http://redmine.lighttpd.net/projects/lighttpd/wiki/Docs:ModSetEnv
Requires:	%{name} = %{version}-%{release}
Provides:	webserver(setenv)

%description mod_setenv
mod_setenv is used to add request headers.

%description mod_setenv -l pl.UTF-8
mod_setenv służy do dodawania nagłówków żądań.

%package mod_simple_vhost
Summary:	lighttpd module for simple virtual-hosting
Summary(pl.UTF-8):	Moduł lighttpd do prostych hostów wirtualnych
Group:		Networking/Daemons/HTTP
URL:		http://redmine.lighttpd.net/projects/lighttpd/wiki/Docs:ModSimpleVhost
Requires:	%{name} = %{version}-%{release}
Conflicts:	%{name}-mod_mysql_vhost

%description mod_simple_vhost
lighttpd module for simple virtual-hosting.

%description mod_simple_vhost -l pl.UTF-8
Moduł lighttpd do prostych hostów wirtualnych.

%package mod_ssi
Summary:	lighttpd module for server-side includes
Summary(pl.UTF-8):	Moduł lighttpd do SSI (server-side includes)
Group:		Networking/Daemons/HTTP
URL:		http://redmine.lighttpd.net/projects/lighttpd/wiki/Docs:ModSSI
Requires:	%{name} = %{version}-%{release}

%description mod_ssi
The module for server-side includes provides a compatability layer for
NSCA/Apache SSI.

%description mod_ssi -l pl.UTF-8
Moduł server-side includes udostępnia warstwę kompatybilności z SSI
znanym z NSCA/Apache'a.

%package mod_staticfile
Summary:	lighttpd module for static file serving
Summary(pl.UTF-8):	Moduł lighttpd do serwowania statycznych plików
Group:		Networking/Daemons/HTTP
Requires:	%{name} = %{version}-%{release}

%description mod_staticfile
lighttpd module for static file serving.

%description mod_staticfile -l pl.UTF-8
Moduł lighttpd do serwowania statycznych plików.

%package mod_status
Summary:	lighttpd module for displaying server status
Summary(pl.UTF-8):	Moduł lighttpd do wyświetlania stanu serwera
Group:		Networking/Daemons/HTTP
URL:		http://redmine.lighttpd.net/projects/lighttpd/wiki/Docs:ModStatus
Requires:	%{name} = %{version}-%{release}

%description mod_status
mod_status displays the server's status and configuration.

%description mod_status -l pl.UTF-8
mod_status wyświetla stan i konfigurację serwera.

%package mod_trigger_b4_dl
Summary:	Trigger before Download
Summary(pl.UTF-8):	Wyzwalacz przed ściąganiem
Group:		Networking/Daemons/HTTP
URL:		http://redmine.lighttpd.net/projects/lighttpd/wiki/Docs:ModTriggerBeforeDownload
Requires:	%{name} = %{version}-%{release}

%description mod_trigger_b4_dl
Another anti hot-linking module.

%description mod_trigger_b4_dl -l pl.UTF-8
Jeszcze jeden moduł blokujący bezpośrednie linkowanie.

%package mod_userdir
Summary:	lighttpd module for user homedirs
Summary(pl.UTF-8):	Moduł lighttpd obsługujący katalogi domowe użytkowników
Group:		Networking/Daemons/HTTP
URL:		http://redmine.lighttpd.net/projects/lighttpd/wiki/Docs:ModUserDir
Requires:	%{name} = %{version}-%{release}

%description mod_userdir
The userdir module provides a simple way to link user-based
directories into the global namespace of the webserver.

%description mod_userdir -l pl.UTF-8
Moduł userdir udostępnia prosty sposób włączenia katalogów
użytkowników do globalnej przestrzeni nazw serwera WWW.

%package mod_usertrack
Summary:	lighttpd usertrack module
Summary(pl.UTF-8):	Moduł usertrack dla lighttpd
Group:		Networking/Daemons/HTTP
URL:		http://redmine.lighttpd.net/projects/lighttpd/wiki/Docs:ModUserTrack
Requires:	%{name} = %{version}-%{release}

%description mod_usertrack
lighttpd usertrack module.

%description mod_usertrack -l pl.UTF-8
Moduł usertrack dla lighttpd.

%package mod_webdav
Summary:	WebDAV module for lighttpd
Summary(pl.UTF-8):	Moduł WebDAV dla libghttpd
Group:		Networking/Daemons/HTTP
URL:		http://redmine.lighttpd.net/projects/lighttpd/wiki/Docs:ModWebDAV
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
- LOCK (experimental)

and the usual GET, POST, HEAD from HTTP/1.1.

So far mounting a webdav resource into Windows XP works and the basic
litmus tests are passed.

%description mod_webdav -l pl.UTF-8
Moduł WebDAV to bardzo minimalistyczna implementacja RFC 2518.
Minimalistyczna oznacza, że jeszcze nie wszystkie operacje są
zaimplementowane. Jak na razie są:
- PROPFIND
- OPTIONS
- MKCOL
- DELETE
- PUT
- LOCK (experimental)

oraz zwykłe GET, POST, HEAD z HTTP/1.1.

Jak na razie montowanie zasobu webdav pod Windows XP działa i
podstawowe testy lakmusowe przechodzą.

%package php-spawned
Summary:	PHP support via FastCGI, spawned by lighttpd
Summary(pl.UTF-8):	Obsługa PHP przez FastCGI, uruchamiane przez lighttpd
Group:		Networking/Daemons/HTTP
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-mod_fastcgi = %{version}-%{release}
Requires:	php(fcgi)
Provides:	webserver(php)
Obsoletes:	lighttpd-php-external

%description php-spawned
PHP support via FastCGI, spawned by lighttpd.

%description php-spawned -l pl.UTF-8
Obsługa PHP przez FastCGI, uruchamiane przez lighttpd.

%package php-external
Summary:	PHP support via FastCGI, spawning controlled externally
Summary(pl.UTF-8):	Obsługa PHP przez FastCGI, uruchamianie sterowane zewnętrznie
Group:		Networking/Daemons/HTTP
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-mod_fastcgi = %{version}-%{release}
Suggests:	php(fpm)
Suggests:	php-fcgi-init
Obsoletes:	lighttpd-php-spawned

%description php-external
PHP support via FastCGI, spawning controlled externally.

%description php-external -l pl.UTF-8
Obsługa PHP przez FastCGI, uruchamianie sterowane zewnętrznie.

%package ssl
Summary:	lighttpd support for SSLv2 and SSLv3
Summary(pl.UTF-8):	Obsługa SSLv2 i SSLv3 dla lighttpd
Group:		Networking/Daemons/HTTP
URL:		http://redmine.lighttpd.net/projects/lighttpd/wiki/Docs:SSL
Requires:	%{name} = %{version}-%{release}
Suggests:	ca-certificates

%description ssl
lighttpd support for SSLv2 and SSLv3.

%description ssl -l pl.UTF-8
Obsługa SSLv2 i SSLv3 dla lighttpd.

%package -n monit-rc-lighttpd
Summary:	lighttpd support for monit
Summary(pl.UTF-8):	Wsparcie lighttpd dla monit
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	monit

%description -n monit-rc-lighttpd
monitrc file for monitoring lighttpd web server.

%description -n monit-rc-lighttpd -l pl.UTF-8
Plik monitrc do monitorowania serwera www lighttpd.

%prep
%setup -q
#%patch100 -p0
%patch0 -p1
%patch1 -p1
%{?with_h264_streaming:%patch2 -p1}
%patch3 -p1
%{?with_deflate:%patch5 -p1}
%patch6 -p1
%patch7 -p1

rm -f src/mod_ssi_exprparser.h # bad patching: should be removed by is emptied instead

# build mime.types.conf
sh %{SOURCE6} /etc/mime.types
cp -p %{SOURCE14} PLD-TODO

%if "%{pld_release}" == "ac"
%{__sed} -i -e 's/ serial_tests//' configure.ac
%{__sed} -i -e 's/dist-xz/dist-bzip2/' configure.ac
%endif

%build
ver=$(awk '/AC_INIT/{a=$2;gsub(/[\[\],]/, "", a); print a}' configure.ac)
if [ "$ver" != "%{version}" ]; then
	: configure.ac specifies wrong version
	exit 1
fi

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
	%{?with_lua:--with-lua=lua51} \
	%{?with_memcache:--with-memcache} \
	%{?with_webdav_props:--with-webdav-props} \
	%{?with_webdav_locks:--with-webdav-locks} \
	%{?with_gamin:--with-gamin} \
	%{?with_gdbm:--with-gdbm}

# -j1 as src/mod_ssi_exprparser.h regeneration deps are broken
%{__make} -j1

%if %{with tests}
export LIGHTTPD_TEST_PORT=$((2048 + RANDOM % 10))
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_lighttpddir}/{cgi-bin,html},/etc/{logrotate.d,rc.d/init.d,sysconfig,monit}} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{conf,vhosts,webapps}.d \
	$RPM_BUILD_ROOT{/var/log/{%{name},archive/%{name}},/var/run/%{name}} \
	$RPM_BUILD_ROOT%{_datadir}/lighttpd/errordocs \
	$RPM_BUILD_ROOT/var/lib/lighttpd \
	$RPM_BUILD_ROOT/var/cache/lighttpd/mod_compress \
	$RPM_BUILD_ROOT{%{systemdtmpfilesdir},%{systemdunitdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -p %{SOURCE2} %{SOURCE3} mime.types.conf $RPM_BUILD_ROOT%{_sysconfdir}
cp -p %{SOURCE4} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}
cp -p %{SOURCE5} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
cp -p %{SOURCE12} $RPM_BUILD_ROOT/etc/monit/%{name}.monitrc
cp -p %{SOURCE16} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf
cp -p %{SOURCE17} $RPM_BUILD_ROOT%{systemdunitdir}/%{name}.service

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# Install lighttpd images
cp -p %{SOURCE7} %{SOURCE8} %{SOURCE9} $RPM_BUILD_ROOT%{_lighttpddir}/html
cp -p %{SOURCE10} $RPM_BUILD_ROOT%{_lighttpddir}/html/pld_button.png
cp -p %{SOURCE11} $RPM_BUILD_ROOT%{_lighttpddir}/html/index.html

# NOTE: the order of the modules is somewhat important as the modules are
# handled in the way they are specified. mod_rewrite should always be the first
# module, mod_accesslog always the last.

conf_available=$RPM_BUILD_ROOT%{_sysconfdir}/conf.d
conf_enabled=../

cp -p %{SOURCE117} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/10_mod_rewrite.conf
cp -p %{SOURCE116} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/11_mod_redirect.conf

cp -p %{SOURCE100} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_access.conf
cp -p %{SOURCE102} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_alias.conf
cp -p %{SOURCE103} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_auth.conf
cp -p %{SOURCE104} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_cgi.conf
cp -p %{SOURCE137} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_cgi_php.conf
cp -p %{SOURCE105} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_cml.conf
cp -p %{SOURCE107} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_deflate.conf
cp -p %{SOURCE108} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_dirlisting.conf
cp -p %{SOURCE109} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_evasive.conf
cp -p %{SOURCE110} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_evhost.conf
cp -p %{SOURCE112} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_fastcgi.conf
cp -p %{SOURCE113} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_flv_streaming.conf
%if %{with h264_streaming}
cp -p %{SOURCE136} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_h264_streaming.conf
%endif
cp -p %{SOURCE114} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_indexfile.conf
cp -p %{SOURCE115} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_proxy.conf
cp -p %{SOURCE118} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_rrdtool.conf
cp -p %{SOURCE119} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_scgi.conf
cp -p %{SOURCE120} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_secdownload.conf
cp -p %{SOURCE121} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_setenv.conf
cp -p %{SOURCE122} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_simple_vhost.conf
cp -p %{SOURCE123} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_ssi.conf
cp -p %{SOURCE124} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_staticfile.conf
cp -p %{SOURCE125} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_status.conf
cp -p %{SOURCE126} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_trigger_b4_dl.conf
cp -p %{SOURCE127} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_userdir.conf
cp -p %{SOURCE128} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_usertrack.conf
cp -p %{SOURCE129} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_webdav.conf
cp -p %{SOURCE133} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/50_mod_mysql_vhost.conf

cp -p %{SOURCE134} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/55_mod_magnet.conf
cp -p %{SOURCE111} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/55_mod_expire.conf

cp -p %{SOURCE106} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/60_mod_compress.conf

cp -p %{SOURCE101} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_mod_accesslog.conf
cp -p %{SOURCE135} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/91_mod_extforward.conf

cp -p %{SOURCE130} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/php-spawned.conf
cp -p %{SOURCE131} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/php-external.conf
cp -p %{SOURCE132} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/ssl.conf

touch $RPM_BUILD_ROOT/var/lib/lighttpd/lighttpd.rrd

install -d $RPM_BUILD_ROOT/etc/tmpwatch
cp -p %{SOURCE138} $RPM_BUILD_ROOT/etc/tmpwatch/lighttpd-mod_compress.conf

%if %{without mysql}
# avoid packaging dummy module
%{__rm} $RPM_BUILD_ROOT%{_libdir}/mod_mysql_vhost.so
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/*_mod_mysql_vhost.conf
%endif
%if %{without deflate}
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/*_mod_deflate.conf
%endif

touch $RPM_BUILD_ROOT/var/log/%{name}/{access,error,breakage}.log

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 109 lighttpd
%groupadd -g 51 http
%useradd -u 116 -d %{_lighttpddir} -c "Lighttpd User" -g lighttpd lighttpd
%addusertogroup lighttpd http

%post
for a in access.log error.log breakage.log; do
	if [ ! -f /var/log/%{name}/$a ]; then
		touch /var/log/%{name}/$a
		chown lighttpd:lighttpd /var/log/%{name}/$a
		chmod 644 /var/log/%{name}/$a
	fi
done
/sbin/chkconfig --add %{name}
%systemd_post %{name}.service

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi
%systemd_preun %{name}.service

%postun
if [ "$1" = "0" ]; then
	%userremove lighttpd
	%groupremove lighttpd
	%groupremove http
fi
%systemd_reload

%posttrans
# minimizing lighttpd restarts logics. we restart webserver:
#
# 1. at the end of transaction. (posttrans, feature from rpm 4.4.2)
# 2. first install of module (post: $1 = 1)
# 2. uninstall of module (postun: $1 = 0)
#
# the strict internal deps between lighttpd modules and
# main package are very important for all this to work.
%service %{name} restart "Lighttpd webserver"
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
%module_scripts mod_extforward
%module_scripts mod_fastcgi
%module_scripts mod_flv_streaming
%module_scripts mod_h264_streaming
%module_scripts mod_indexfile
%module_scripts mod_magnet
%module_scripts mod_mysql_vhost
%module_scripts mod_proxy
%module_scripts mod_redirect
%module_scripts mod_rewrite

%post mod_rrdtool
if [ ! -f /var/lib/lighttpd/lighttpd.rrd ]; then
	touch /var/lib/lighttpd/lighttpd.rrd
	chown lighttpd:stats /var/lib/lighttpd/lighttpd.rrd
	chmod 640 /var/lib/lighttpd/lighttpd.rrd
fi
%module_post

%postun mod_rrdtool
%module_postun

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

%triggerpostun -- %{name} < 1.4.18-10.1
if [ -f /etc/lighttpd/conf.d/50_mod_extforward.conf.rpmsave ]; then
	cp -f /etc/lighttpd/conf.d/91_mod_extforward.conf{,.rpmnew}
	mv -f /etc/lighttpd/conf.d/{50_mod_extforward.conf.rpmsave,91_mod_extforward.conf}
fi

%files
%defattr(644,root,root,755)
%doc NEWS README PLD-TODO
%dir %attr(751,root,lighttpd) %{_sysconfdir}
%dir %attr(750,root,root) %{_sysconfdir}/conf.d
%dir %attr(750,root,root) %{_sysconfdir}/vhosts.d
%dir %attr(750,root,root) %{_sysconfdir}/webapps.d
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mime.types.conf
%attr(640,root,lighttpd) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.user

%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%attr(750,root,root) %dir /var/log/archive/%{name}
%dir %attr(751,root,root) /var/log/%{name}
%attr(644,lighttpd,lighttpd) %ghost /var/log/%{name}/access.log
%attr(644,lighttpd,lighttpd) %ghost /var/log/%{name}/error.log
%attr(644,lighttpd,lighttpd) %ghost /var/log/%{name}/breakage.log
%dir %attr(770,root,lighttpd) /var/run/%{name}
%{systemdtmpfilesdir}/%{name}.conf
%{systemdunitdir}/%{name}.service
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/*
%attr(755,root,root) %{_sbindir}/lighttpd
%attr(755,root,root) %{_sbindir}/lighttpd-angel
%dir %{_libdir}
%{_mandir}/man8/lighttpd.8*
%dir %{_lighttpddir}
%dir %{_lighttpddir}/cgi-bin
%dir %{_lighttpddir}/html
%config(noreplace,missingok) %verify(not md5 mtime size) %{_lighttpddir}/html/index.html
%config(missingok) %verify(not md5 mtime size) %{_lighttpddir}/html/*.png
%config(missingok) %verify(not md5 mtime size) %{_lighttpddir}/html/*.ico

%dir %{_datadir}/lighttpd
%dir %{_datadir}/lighttpd/errordocs

# rrdtool database is stored there
%dir %attr(771,root,lighttpd) /var/lib/lighttpd

# mod_compress can put cached files there
%dir /var/cache/lighttpd

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

%files mod_cgi_php
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_cgi_php.conf

%files mod_cml
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_cml.conf
%attr(755,root,root) %{_libdir}/mod_cml.so

%files mod_compress
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/tmpwatch/lighttpd-mod_compress.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_compress.conf
%attr(755,root,root) %{_libdir}/mod_compress.so
%dir %attr(775,root,lighttpd) /var/cache/lighttpd/mod_compress

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

%files mod_extforward
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_extforward.conf
%attr(755,root,root) %{_libdir}/mod_extforward.so

%files mod_fastcgi
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_fastcgi.conf
%attr(755,root,root) %{_libdir}/mod_fastcgi.so

%files mod_flv_streaming
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_flv_streaming.conf
%attr(755,root,root) %{_libdir}/mod_flv_streaming.so

%if %{with h264_streaming}
%files mod_h264_streaming
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_h264_streaming.conf
%attr(755,root,root) %{_libdir}/mod_h264_streaming.so
%endif

%files mod_indexfile
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_indexfile.conf
%attr(755,root,root) %{_libdir}/mod_indexfile.so

%files mod_magnet
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_magnet.conf
%attr(755,root,root) %{_libdir}/mod_magnet.so

%if %{with mysql}
%files mod_mysql_vhost
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_mysql_vhost.conf
%attr(755,root,root) %{_libdir}/mod_mysql_vhost.so
%endif

%files mod_proxy
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*mod_proxy.conf
%attr(755,root,root) %{_libdir}/mod_proxy.so

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
%attr(640,lighttpd,stats) %ghost /var/lib/lighttpd/lighttpd.rrd

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

%files php-spawned
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/php-spawned.conf

%files php-external
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/php-external.conf

%files ssl
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/ssl.conf

%files -n monit-rc-lighttpd
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/monit/%{name}.monitrc
