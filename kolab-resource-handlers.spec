%define _enable_debug_packages %{nil}
%define debug_package          %{nil}
%define __noautoreq /usr/bin/php

%define kolab_webroot /var/www/html/kolab

#% define _requires_exceptions pear(Horde

# the Management user/group name/id pair
# These are created in the kolab package, which
# we prereq
%define l_musr kolab
%define l_mgrp kolab

# the Restricted user/group name/id pair
%define l_rusr %{l_musr}
%define l_rgrp %{l_mgrp}

# the Non-privileged user/group name/id pair
%define l_nusr %{l_musr}
%define l_ngrp %{l_mgrp}

Summary:	Kolab components for group and resource management

Name:		kolab-resource-handlers
Version:	2.1.0
Release:	12
License:	GPL
Group:		System/Servers
URL:		https://www.kolab.org/
Source0:	kolab-resource-handlers-%{version}.tar.bz2
Source1:	mandriva
# php5 doesn't have the domxml extension anymore. This patch makes
# freebusy use the dom extension, available in PHP5.
Patch0:		kolab-resource-handlers-phpdom.diff
Requires(post):	rpm-helper
Requires(preun): rpm-helper
Requires(pre):	rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.4
Requires(pre):	apache-mod_php
Requires(pre):	apache-mpm >= 2.2.4
Requires(pre):	kolab >= 2.1.0
Requires(pre):	kolab-horde-framework >= 2.1.0
Requires:	apache-conf >= 2.2.4
Requires:	apache-mod_php
Requires:	apache-mpm >= 2.2.4
Requires:	kolab >= 2.1.0
Requires:	kolab-horde-framework >= 2.1.0
Requires:	php-dba
Requires:	php-dom
Requires:	php-fileinfo
Requires:	php-gd
Requires:	php-iconv
Requires:	php-mbstring
Requires:	php-mcal
Requires:	php-mcrypt
BuildArch:	noarch

%description
Kolab components for group and resource management.

%prep

%setup -q -n %{name}-%{version}
%patch0 -p0

cp %{SOURCE1} dist_conf/mandriva

# hard code some paths
find -type f | xargs perl -pi -e "s|\@kolab_php_module_prefix\@freebusy/|%{kolab_webroot}/freebusy/|g" 
find -type f | xargs perl -pi -e "s|\@kolab_php_module_prefix\@kolabfilter/|%{kolab_webroot}/kolabfilter/|g" 
find -type f | xargs perl -pi -e "s|\@webserver_document_root\@|%{kolab_webroot}|g" 
	
# cleanup
for i in `find . -type d -name CVS`  `find . -type d -name .svn` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

%configure2_5x \
    --with-dist=mandriva

%make

%install
%makeinstall_std

install -d %{buildroot}%{_localstatedir}/lib/kolab/resmgr/filter
install -d %{buildroot}%{_localstatedir}/lib/kolab/freebusy/cache

# cleanup
rm -rf %{buildroot}%{_datadir}/doc/kolab

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart 1>&2
    fi
fi

%files
%doc AUTHORS COPYING ChangeLog INSTALL NEWS
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/kolab/resmgr/freebusy.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/kolab/resmgr/resmgr.conf
%attr(0700,%{l_musr},%{l_mgrp}) %dir %{_localstatedir}/lib/kolab/resmgr
%attr(0700,%{l_musr},%{l_mgrp}) %dir %{_localstatedir}/lib/kolab/resmgr/filter
%attr(0755,root,root) %dir %{kolab_webroot}/freebusy
%attr(0755,root,root) %dir %{kolab_webroot}/kolabfilter
%attr(0644,root,root) %{kolab_webroot}/freebusy/*.php
%attr(0644,root,root) %{kolab_webroot}/kolabfilter/*.php
%attr(0755,%{l_musr},%{l_mgrp}) %dir %{_datadir}/kolab/scripts/resmgr
%attr(0755,root,root) %{_datadir}/kolab/scripts/resmgr/kolabfilter.php
%attr(0755,root,root) %{_datadir}/kolab/scripts/resmgr/kolabmailboxfilter.php
%attr(0770,apache,apache) %dir %{_localstatedir}/lib/kolab/freebusy/cache


