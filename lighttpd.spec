# TODO:
# - fix SSL build
Summary:	Fast as light http server
Summary(pl):	Szybki i lekki serwer http
Name:		lighttpd
Version:	1.1.2a
Release:	0.1
Group:		Networking/Daemons
License:	GPL
Source0:	http://jan.kneschke.de/projects/lighttpd/download/%{name}-%{version}.tar.gz
# Source0-md5:	2b5d247d2f62ac5255fa711a0c85bf06
Source1:	%{name}.init
URL:		http://jan.kneschke.de/projects/lighttpd/
Provides:	httpd
Provides:	webserver
PreReq:		rc-scripts
Requires(pre):	sh-utils
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/userdel
Requires(postun):	/usr/sbin/groupdel
BuildRequires:	mysql-devel
BuildRequires:	zlib-devel
BuildRequires:	bzip2-devel
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir		%{_prefix}/%{_lib}/%{name}
%define		_sysconfdir	/etc/%{name}

%description
ighttpd a secure, fast, compliant and very flexible web-server which
has been optimized for high-performance environments. It has a very
low memory footprint compared to other webservers and takes care of
cpu-load. Its advanced feature-set (FastCGI, CGI, Auth,
Output-Compression, URL-Rewriting and many more) make lighttpd the
perfect webserver-software for every server that is suffering load
problems.

%prep
%setup -q

%build
%configure \
	--enable-mod-chat \
	--enable-mod-cache \
	--enable-mod-localizer \
	--with-mysql \
	--without-ssl
	
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/home/httpd/cgi-bin,/etc/{rc.d/init.d,%{name}}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install doc/lighttpd.{conf,user} $RPM_BUILD_ROOT%{_sysconfdir}

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
	/usr/sbin/useradd -u 51 -r -d /home/httpd -s /bin/false -c "HTTP User" -g http http 1>&2
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
%attr(644,root,root) %{_libdir}/*.a
%attr(-, http, http) /home/httpd
%attr(754,root,root) /etc/rc.d/init.d/lighttpd
%dir %attr(754,root,root) /etc/%{name}
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*.*
%{_mandir}/man?/*
