%define		subver RC1
Summary:	PHP interface for verlihub
Summary(pl):	Interfejs php dla verlihub
Name:		verliadmin
Version:	0.3_%{subver}
Release:	1
License:	GPL
Group:		Networking/Admin
Source0:	http://dl.sourceforge.net/verlihub/VerliAdmin_%{version}.zip
# Source0-md5:	507a133edf72a4c68ba967dac91b1e76
URL:		http://bohyn.czechweb.cz/
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

# workaround for ugly sources
mv -f ../VERLIADMIN/* .
rm -rf ../VERLIADMIN

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_httpdir}/verliadmin/{img,language,logs}

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
%{_httpdir}/verliadmin/[abdefhiklmrsuv]*.php
%{_httpdir}/verliadmin/commands.php
%{_httpdir}/verliadmin/chpass.php
%attr(640,root,http) %verify(not md5 size mtime) %config(noreplace) %{_httpdir}/verliadmin/config.php
