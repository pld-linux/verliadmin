%define		subver RC3
Summary:	PHP interface for verlihub
Summary(pl):	Interfejs php dla verlihub
Name:		verliadmin
Version:	0.3
Release:	1.%{subver}
Epoch:		1
License:	GPL
Group:		Networking/Admin
Source0:	http://bohyn.czechweb.cz/download/VerliAdmin_%{version}_%{subver}.zip
# Source0-md5:	efb8c1a2e89c3d2652e184931ca273af
URL:		http://bohyn.czechweb.cz/
BuildRequires:	unzip
Requires:	verlihub = 0.9.7
Requires:	php
Requires:	webserver
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_httpdir	/home/services/httpd/html

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

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_httpdir}/verliadmin/{img,language,logs}

install favicon.ico $RPM_BUILD_ROOT%{_httpdir}/verliadmin
install default.css $RPM_BUILD_ROOT%{_httpdir}/verliadmin
install *.php $RPM_BUILD_ROOT%{_httpdir}/verliadmin
install img/* $RPM_BUILD_ROOT%{_httpdir}/verliadmin/img
install language/* $RPM_BUILD_ROOT%{_httpdir}/verliadmin/language

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc readme.txt *.sql
%dir %{_httpdir}/verliadmin
%{_httpdir}/verliadmin/img
%{_httpdir}/verliadmin/language
%{_httpdir}/verliadmin/logs
%{_httpdir}/verliadmin/[abdefhiklmrsuv]*.*
%{_httpdir}/verliadmin/commands.php
%{_httpdir}/verliadmin/chpass.php
%attr(640,root,http) %verify(not md5 size mtime) %config(noreplace) %{_httpdir}/verliadmin/config.php
