Summary:	PHP interface for verlihub
Summary(pl.UTF-8):	Interfejs PHP dla verlihub
Name:		verliadmin
Version:	0.3
Release:	8
Epoch:		1
License:	GPL
Group:		Networking/Admin
Source0:	http://bohyn.czechweb.cz/download/VerliAdmin_%{version}.zip
# Source0-md5:	6f39fd52150c6218dc20e115a65a08a4
Patch0:		%{name}-lang.patch
URL:		http://bohyn.czechweb.cz/
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
Requires:	verlihub >= 0.9.7
Requires:	webapps
Requires:	webserver
Requires:	webserver(php)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_verliadmindir	%{_datadir}/%{name}
%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}

%description
Verliadmin is administration tool for verlihub written in php. All
configuration values are in MySQL database and in defaultconf.php. In
config.php you must setup MySQL connection. Everyting else is
predefined.

%description -l pl.UTF-8
Verliadmin jest narzędziem administracyjnym dla verlihuba napisanym w
php. Wszystkie wartości konfiguracji są w bazie MySQL oraz w pliku
defaultconf.php. W pliku config.php należy ustawić parametry
połączenia z MySQL.

%prep
%setup -q -n VerliAdmin
%patch -P0 -p1

# undos the source
find . -type f -print0 | xargs -0 sed -i -e 's,\r$,,'

cat <<'EOF' > apache.conf
Alias /verliadmin %{_datadir}/%{name}
<Directory %{_datadir}/%{name}>
	Allow from all
</Directory>
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_verliadmindir}/{img,language},%{_sysconfdir}}

install favicon.ico $RPM_BUILD_ROOT%{_verliadmindir}
install default.css $RPM_BUILD_ROOT%{_verliadmindir}
mv config.php $RPM_BUILD_ROOT%{_sysconfdir}
install *.php $RPM_BUILD_ROOT%{_verliadmindir}
install img/* $RPM_BUILD_ROOT%{_verliadmindir}/img
install language/* $RPM_BUILD_ROOT%{_verliadmindir}/language
ln -sf %{_sysconfdir}/config.php $RPM_BUILD_ROOT%{_verliadmindir}/config.php

# for apache
install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- verliadmin < 1:0.3-2.1
# rescue app config
if [ -f /home/servicves/httpd/html/verliadmin/config.php.rpmsave ]; then
	mv -f %{_sysconfdir}/config.php{,.rpmnew}
	mv -f /home/servicves/httpd/html/verliadmin/config.php.rpmsave %{_sysconfdir}/config.php
fi
if [ -f /etc/%{name}/config.php.rpmsave ]; then
	mv -f %{_sysconfdir}/config.php{,.rpmnew}
	mv -f /etc/%{name}/config.php.rpmsave %{_sysconfdir}/config.php
fi

# migrate from apache-config macros
if [ -f /etc/%{name}/apache-%{name}.conf.rpmsave ]; then
	if [ -d /etc/apache/webapps.d ]; then
		cp -f %{_sysconfdir}/apache.conf{,.rpmnew}
		cp -f /etc/%{name}/apache-%{name}.conf.rpmsave %{_sysconfdir}/apache.conf
	fi

	if [ -d /etc/httpd/webapps.d ]; then
		cp -f %{_sysconfdir}/httpd.conf{,.rpmnew}
		cp -f /etc/%{name}/apache-%{name}.conf.rpmsave %{_sysconfdir}/httpd.conf
	fi
	rm -f /etc/%{name}/apache-%{name}.conf.rpmsave
fi

# migrating from earlier apache-config?
if [ -L /etc/apache/conf.d/99_%{name}.conf ]; then
	rm -f /etc/apache/conf.d/99_%{name}.conf
	apache_reload=1
fi
if [ -L /etc/httpd/httpd.conf/99_%{name}.conf ]; then
	rm -f /etc/httpd/httpd.conf/99_%{name}.conf
	httpd_reload=1
fi

if [ "$httpd_reload" ]; then
	/usr/sbin/webapp register httpd %{_webapp}
	%service -q httpd reload
fi
if [ "$apache_reload" ]; then
	/usr/sbin/webapp register apache %{_webapp}
	%service -q apache reload
fi

%files
%defattr(644,root,root,755)
%doc readme.txt scripts/*.sql
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config.php
%{_verliadmindir}
