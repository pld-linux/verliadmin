Summary:	PHP interface for verlihub
Summary(pl):	Interfejs PHP dla verlihub
Name:		verliadmin
Version:	0.3
Release:	1
Epoch:		1
License:	GPL
Group:		Networking/Admin
Source0:	http://bohyn.czechweb.cz/download/VerliAdmin_%{version}.zip
# Source0-md5:	6f39fd52150c6218dc20e115a65a08a4
Patch0:		%{name}-lang.patch
URL:		http://bohyn.czechweb.cz/
BuildRequires:	unzip
Requires:	verlihub >= 0.9.7
Requires:	php
Requires:	webserver
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_verliadmindir	%{_datadir}/%{name}

%description
Verliadmin is administration tool for verlihub written in php.
All configuration values are in MySQL database and in defaultconf.php.
In config.php you must setup MySQL connection. Everyting else is predefined.

%description -l pl
Verliadmin jest narzêdziem administracyjnym dla verlihuba napisanym w php.
Wszystkie warto¶ci konfiguracji s± w bazie MySQL oraz w pliku defaultconf.php.
W pliku config.php nale¿y ustawiæ parametry po³±czenia z MySQL.

%prep
%setup -q -n VerliAdmin
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_verliadmindir}/{img,language},%{_sysconfdir}/{verliadmin,httpd}}

install favicon.ico $RPM_BUILD_ROOT%{_verliadmindir}
install default.css $RPM_BUILD_ROOT%{_verliadmindir}
mv config.php $RPM_BUILD_ROOT%{_sysconfdir}/verliadmin
install *.php $RPM_BUILD_ROOT%{_verliadmindir}
install img/* $RPM_BUILD_ROOT%{_verliadmindir}/img
install language/* $RPM_BUILD_ROOT%{_verliadmindir}/language
ln -sf %{_sysconfdir}/verliadmin/config.php $RPM_BUILD_ROOT%{_verliadmindir}/config.php

# for apache
echo "Alias /verliadmin /usr/share/%{name}" >%{name}.conf
install %{name}.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*%{name}.conf" /etc/httpd; then
	echo "Include /etc/httpd/%{name}.conf" >> /etc/httpd/httpd.conf
elif [ -d /etc/httpd/httpd.conf ]; then
	ln -sf /etc/httpd/%{name}.conf /etc/httpd/httpd.conf/99_%{name}.conf
fi
if [ -f /var/lock/subsys/httpd ]; then
	/usr/sbin/apachectl restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	umask 027
	if [ -d /etc/httpd/httpd.conf ]; then
		rm -f /etc/httpd/httpd.conf/99_%{name}.conf
	else
		grep -v "^Include.*%{name}.conf" /etc/httpd/httpd.conf > \
			/etc/httpd/httpd.conf.tmp
		mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
		if [ -f /var/lock/subsys/httpd ]; then
			/usr/sbin/apachectl restart 1>&2
		fi
	fi
fi

%triggerin -- verliadmin = 0.3_RC1
mv -f /home/services/httpd/html/verliadmin/config.php %{_sysconfdir}/verliadmin/config.php

%files
%defattr(644,root,root,755)
%doc readme.txt scripts/*.sql
%{_verliadmindir}
%attr(750,root,http) %dir %{_sysconfdir}/verliadmin/
%attr(640,root,http) %verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/verliadmin/config.php
%config(noreplace) %verify(not size mtime md5) /etc/httpd/%{name}.conf
