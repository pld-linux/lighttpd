# TODO:
# - fix SSL build
Summary:	Fast and light http server
Summary(pl):	Szybki i lekki serwer http
Name:		lighttpd
Version:	1.1.6
Release:	0.1
Group:		Networking/Daemons
License:	QPL
Source0:	http://jan.kneschke.de/projects/lighttpd/download/%{name}-%{version}.tar.gz
# Source0-md5:	b4b52995be279ee7e687eacedb3e8190
Source1:	%{name}.init
Source2:	%{name}.conf
Source3:	%{name}.user
Patch0:		%{name}-configure.patch
Patch1:		%{name}-sendfile.patch
URL:		http://jan.kneschke.de/projects/lighttpd/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	libtool
BuildRequires:	mysql-devel
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel
BuildRequires:	zlib-devel
PreReq:		rc-scripts
Requires(pre):	sh-utils
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/userdel
Requires(postun):	/usr/sbin/groupdel
Provides:	httpd
Provides:	webserver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir		%{_prefix}/%{_lib}/%{name}
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
serwerem WWW, kt�ry zosta� zoptymalizowany pod k�tem
wysokowydajno�ciowych �rodowisk. Zajmuje bardzo ma�� ilo�� pami�ci
w por�wnaniu do innych serwer�w WWW oraz dba o zaj�to�� procesora.
Szeroki zestaw opcji (FastCGI, CGI, uwierzytelnianie, kompresja
wyj�cia, przepisywanie URL-i i wiele innych) czyni� z lighttpd
doskona�e oprogramowanie web-serwerowe na ka�dy serwer cierpi�cy
z powodu problem�w z obci��eniem.

%prep
%setup -q
%patch0 -p0
%patch1 -p0

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--enable-mod-chat \
	--enable-mod-cache \
	--enable-mod-localizer \
	--with-mysql \
	--without-ssl
	
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/home/services/httpd/cgi-bin,/var/log/%{name},/etc/{rc.d/init.d,%{name}}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`getgid http`" ]; then
	if [ "`getgid http`" != "51" ]; then
		echo "Error: group http doesn't have gid=51. Correct this before installing %{name}." 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -g 51 -r -f http
fi
if [ -n "`id -u http 2>/dev/null`" ]; then
	if [ "`id -u http`" != "51" ]; then
		echo "Error: user http doesn't have uid=51. Correct this before installing %{name}." 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -u 51 -r -d /home/services/httpd -s /bin/false -c "HTTP User" -g http http 1>&2
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
	/usr/sbin/userdel http
	/usr/sbin/groupdel http
fi

%files
%defattr(644,root,root,755)
%doc NEWS README doc/*.txt
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}
%attr(755,root,root) %{_libdir}/*.so
%dir %attr(750,root,root) /var/log/%{name}
%attr(-, http, http) /home/services/httpd
%attr(754,root,root) /etc/rc.d/init.d/lighttpd
%dir %attr(754,root,root) /etc/%{name}
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*.*
%{_mandir}/man?/*
