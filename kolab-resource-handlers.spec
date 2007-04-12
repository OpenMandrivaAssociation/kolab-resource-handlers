%define snap 20050910

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

%define kolab_webroot /var/www/html/kolab

# undefining these makes the build _real_ quick
%undefine __find_provides
%undefine __find_requires

Summary:	Kolab components for group and resource management
Name:		kolab-resource-handlers
Version:	0.4.1
Release:	%mkrel 0.%{snap}.2
License:	GPL
Group:		System/Servers
URL:		http://www.kolab.org/
Source0:	kolab-resource-handlers-%{version}-%{snap}.tar.bz2
# php5 doesn't have the domxml extension anymore. This patch makes
# freebusy use the dom extension, available in PHP5.
Patch:		kolab-resource-handlers-0.4.1-20050811-phpdom.patch
Patch1:		kolab-resource-handlers-0.4.1-20050811-fbviewroot.patch
# $PHP_SELF only exists if register_globals = on, so let's use $_SERVER['PHP_SELF']
# instead
Patch2:		kolab-resource-handlers-0.4.1-20050811-phpself.patch
BuildRequires:	php php-pear
Requires(post):	rpm-helper
Requires(preun): rpm-helper
Requires(pre):	rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.0.54 apache-mpm-prefork >= 2.0.54 apache-mod_php
Requires(pre):	kolab >= 1.9.5
Requires:	kolab >= 1.9.5
Requires:	apache-conf >= 2.0.54 apache-mpm-prefork >= 2.0.54 apache-mod_php
Requires:	php-dom php-mcrypt php-iconv php-mbstring php-gd php-mcal php-fileinfo php-smarty php-pear-Net_Sieve
Requires:	php-dba php-pear-Date php-pear-HTTP_Request
# (oe) these conflicts with the ones we have and no time to review or test
Conflicts:	php-pear-File_PDF php-pear-Net_Cyrus php-pear-Net_IMAP php-pear-Net_SMS
Conflicts:	php-pear-Text_Diff php-pear-VFS php-pear-XML_SVG
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
Kolab components for group and resource management.

%prep

%setup -q -n kolab-resource-handlers
%patch -p1 -b .phpdom
%patch1 -p1 -b .fbviewroot
%patch2 -p1 -b .phpself

# fix attribs
find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;
	
# cleanup
for i in `find . -type d -name CVS`  `find . -type d -name .svn` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

rm -f Calendar.* kolab-resource-handlers.spec Makefile

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

# major search and replace (aka openpkg anti borker)
find . -type f|xargs perl -pi -e "s|/kolab/var/resmgr/resmgr\.log|/var/log/kolab/resmgr\.log|g; \
    s|/kolab/var/resmgr/freebusy\.log|/var/log/kolab/freebusy\.log|g; \
    s|/kolab/var/resmgr/fbview\.log|/var/log/kolab/fbview\.log|g; \
    s|/kolab/var/resmgr/filter|/var/spool/resmgr/filter|g; \
    s|/kolab/var/kolab/www/fbview|%{kolab_webroot}/fbview|g; \
    s|/var/kolab/www|/var/www/html/kolab|g; \
    s|/kolab/etc/kolab|/etc/kolab|g; \
    s|/kolab/etc/resmgr|/etc/kolab/resmgr|g; \
    s|\@l_prefix\@/var/kolab/php:\@l_prefix\@/var/kolab/php/pear|%{kolab_webroot}|g; \
    s|\@l_prefix\@/bin/php|%{_bindir}/php|g; \
    s|\@l_prefix\@/bin/pear|%{_bindir}/pear|g; \
    s|\@l_prefix\@/etc/resmgr/resmgr\.conf|/etc/kolab/resmgr/resmgr\.conf|g; \
    s|\@l_prefix@/etc/resmgr/freebusy\.conf|/etc/kolab/resmgr/freebusy\.conf|g; \
    s|\@l_prefix\@/var/resmgr/filter|/var/spool/resmgr/filter|g; \
    s|/usr/local/bin/php|%{_bindir}/php|g; \
    s|/kolab/bin/php|%{_bindir}/php|g; \
    s|/usr/local/bin|%{_bindir}|g"

# fix uid and gid
# the Management user/group name/id pair
find . -type f|xargs perl -pi -e "s|\@l_musr\@|%{l_musr}|g;s|\@l_mgrp\@|%{l_mgrp}|g"

# the Rrestricted user/group name/id pair
find . -type f|xargs perl -pi -e "s|\@l_rgrp\@|%{l_rgrp}|g;s|\@l_rusr\@|%{l_rusr}|g"

# the Non-privileged user/group name/id pair
find . -type f|xargs perl -pi -e "s|\@l_nusr\@|%{l_nusr}|g;s|\@l_ngrp\@|%{l_ngrp}|g"

%build

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d
install -d %{buildroot}%{_sysconfdir}/kolab/resmgr
install -d %{buildroot}%{_sysconfdir}/kolab/templates
install -d %{buildroot}/var/spool/resmgr/filter
install -d %{buildroot}%{kolab_webroot}/fbview
install -d %{buildroot}%{kolab_webroot}/freebusy/cache
install -d %{buildroot}%{kolab_webroot}/kolabfilter
install -d %{buildroot}%{kolab_webroot}/locks

install -m0755 kolab-resource-handlers/resmgr/kolabfilter.php %{buildroot}%{_sysconfdir}/kolab/resmgr/
install -m0755 kolab-resource-handlers/resmgr/kolabmailboxfilter.php %{buildroot}%{_sysconfdir}/kolab/resmgr/

install -m0644 kolab-resource-handlers/freebusy/freebusycache.class.php %{buildroot}%{kolab_webroot}/freebusy/
install -m0644 kolab-resource-handlers/freebusy/freebusy.class.php %{buildroot}%{kolab_webroot}/freebusy/
install -m0644 kolab-resource-handlers/freebusy/freebusycollector.class.php %{buildroot}%{kolab_webroot}/freebusy/
install -m0644 kolab-resource-handlers/freebusy/freebusyldap.class.php %{buildroot}%{kolab_webroot}/freebusy/
install -m0644 kolab-resource-handlers/freebusy/misc.php %{buildroot}%{kolab_webroot}/freebusy/
install -m0644 kolab-resource-handlers/freebusy/recurrence.class.php %{buildroot}%{kolab_webroot}/freebusy/
install -m0644 kolab-resource-handlers/freebusy/freebusy.php %{buildroot}%{kolab_webroot}/freebusy/
install -m0644 kolab-resource-handlers/freebusy/pfb.php %{buildroot}%{kolab_webroot}/freebusy/

install -m0644 kolab-resource-handlers/resmgr/kolabmailtransport.php %{buildroot}%{kolab_webroot}/kolabfilter/
install -m0644 kolab-resource-handlers/resmgr/misc.php %{buildroot}%{kolab_webroot}/kolabfilter/
install -m0644 kolab-resource-handlers/resmgr/olhacks.php %{buildroot}%{kolab_webroot}/kolabfilter/
install -m0644 kolab-resource-handlers/resmgr/resmgr.php %{buildroot}%{kolab_webroot}/kolabfilter/

cp -aRf kolab-resource-handlers/fbview/fbview/* %{buildroot}%{kolab_webroot}/fbview/

install -d %{buildroot}%{_datadir}/pear
pushd %{buildroot}%{kolab_webroot}/fbview/framework
    %{_bindir}/php ./install-packages.php --install-dir %{buildroot}%{_datadir}/pear
popd

cat > kolab-resource-handlers.conf << EOF

<Directory "%{kolab_webroot}/fbview/config">
    order deny,allow
    deny from all
</Directory>

<Directory "%{kolab_webroot}/fbview/kronolith/config">
    order deny,allow
    deny from all
</Directory>

<Directory "%{kolab_webroot}/fbview/turba/config">
    order deny,allow
    deny from all
</Directory>

<Directory "%{kolab_webroot}/fbview/admin/locale">
    order deny,allow
    deny from all
</Directory>

<Directory "%{kolab_webroot}/fbview/kronolith/locale">
    order deny,allow
    deny from all
</Directory>

<Directory "%{kolab_webroot}/fbview/locale">
    order deny,allow
    deny from all
</Directory>

<Directory "%{kolab_webroot}/fbview/turba/locale">
    order deny,allow
    deny from all
</Directory>

<Directory "%{kolab_webroot}/fbview/kronolith/po">
    order deny,allow
    deny from all
</Directory>

<Directory "%{kolab_webroot}/fbview/po">
    order deny,allow
    deny from all
</Directory>

<Directory "%{kolab_webroot}/fbview/turba/po">
    order deny,allow
    deny from all
</Directory>

<Directory "%{kolab_webroot}/fbview/kronolith/scripts">
    order deny,allow
    deny from all
</Directory>

<Directory "%{kolab_webroot}/fbview/scripts">
    order deny,allow
    deny from all
</Directory>

<Directory "%{kolab_webroot}/fbview/turba/scripts">
    order deny,allow
    deny from all
</Directory>

<Directory "%{kolab_webroot}/fbview/kronolith/templates">
    order deny,allow
    deny from all
</Directory>

<Directory "%{kolab_webroot}/fbview/templates">
    order deny,allow
    deny from all
</Directory>

<Directory "%{kolab_webroot}/fbview/turba/templates">
    order deny,allow
    deny from all
</Directory>

<Directory "%{kolab_webroot}/fbview/lib">
    order deny,allow
    deny from all
</Directory>

<Directory "%{kolab_webroot}/fbview/kronolith/lib">
    order deny,allow
    deny from all
</Directory>

<Directory "%{kolab_webroot}/fbview/turba/lib">
    order deny,allow
    deny from all
</Directory>

EOF

install -m0644 kolab-resource-handlers.conf %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/kolab-resource-handlers.conf

# fix docs
rm -rf fbview kronolith turba
cp -rp %{buildroot}%{kolab_webroot}/fbview/docs fbview
cp -rp %{buildroot}%{kolab_webroot}/fbview/kronolith/docs kronolith
cp -rp %{buildroot}%{kolab_webroot}/fbview/turba/docs turba

# fix config (if needed)
pushd %{buildroot}%{kolab_webroot}/fbview/config
    for f in *.dist; do
	if ! [ -f ${f%.dist} ]; then cp $f ${f%.dist}; fi
    done
popd

pushd %{buildroot}%{kolab_webroot}/fbview/turba/config
    for f in *.dist; do
	if ! [ -f ${f%.dist} ]; then cp $f ${f%.dist}; fi
    done
popd

pushd %{buildroot}%{kolab_webroot}/fbview/kronolith/config
    for f in *.dist; do
	if ! [ -f ${f%.dist} ]; then cp $f ${f%.dist}; fi
    done
popd

# cleanup
rm -rf %{buildroot}%{kolab_webroot}/fbview/packaging
rm -rf %{buildroot}%{kolab_webroot}/fbview/kronolith/packaging

rm -rf %{buildroot}%{kolab_webroot}/fbview/framework
rm -f %{buildroot}%{_datadir}/pear/.filemap
rm -f %{buildroot}%{_datadir}/pear/.lock

find %{buildroot} -type f -name "\.htaccess"|xargs rm -f
find %{buildroot} -type f -name "COPYING"|xargs rm -f

find %{buildroot} -type f -name "*.dis" | xargs rm -f
find %{buildroot} -type f -name "*.sq" | xargs rm -f
find %{buildroot} -type f -name "*.s" | xargs rm -f
find %{buildroot} -type f -name "*.ph" | xargs rm -f

rm -f %{buildroot}%{kolab_webroot}/fbview/config/*.dis*

# user/groups are created in the kolab package
#%pre
#if getent group %{l_musr} >/dev/null 2>&1 ; then : ; else \
#    /usr/sbin/groupadd -g %{l_mgid} %{l_musr} > /dev/null 2>&1 || exit 1 ; fi
#if getent passwd %{l_musr} >/dev/null 2>&1 ; then : ; else \
#    /usr/sbin/useradd -u %{l_muid} -g %{l_mgid} -M -r -s /bin/bash -c "kolab system user" \
#    -d %{_localstatedir}/kolab %{l_musr} 2> /dev/null || exit 1 ; fi

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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc fbview kronolith turba
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/kolab-resource-handlers.conf
%attr(0755,root,root) %{_sysconfdir}/kolab/resmgr/kolabfilter.php
%attr(0755,root,root) %{_sysconfdir}/kolab/resmgr/kolabmailboxfilter.php
%attr(0700,%{l_musr},%{l_mgrp}) %dir /var/spool/resmgr
%attr(0700,%{l_musr},%{l_mgrp}) %dir /var/spool/resmgr/filter
%attr(0755,root,root) %dir %{kolab_webroot}
%attr(0755,root,root) %dir %{kolab_webroot}/fbview
%attr(0755,root,root) %dir %{kolab_webroot}/kolabfilter
%attr(0755,root,root) %dir %{kolab_webroot}/freebusy
%attr(0770,apache,apache) %dir %{kolab_webroot}/freebusy/cache
%attr(0770,apache,apache) %dir %{kolab_webroot}/locks
%exclude %{kolab_webroot}/fbview/docs
%exclude %{kolab_webroot}/fbview/kronolith/docs
%exclude %{kolab_webroot}/fbview/turba/docs
%{kolab_webroot}/fbview/*
%attr(0640,root,apache) %config(noreplace) %{kolab_webroot}/fbview/config/*.php
%attr(0640,root,apache) %config(noreplace) %{kolab_webroot}/fbview/config/*.xml
%attr(0640,root,apache) %config(noreplace) %{kolab_webroot}/fbview/turba/config/*.php
%attr(0640,root,apache) %config(noreplace) %{kolab_webroot}/fbview/turba/config/*.xml
%attr(0640,root,apache) %config(noreplace) %{kolab_webroot}/fbview/kronolith/config/*.php
%attr(0640,root,apache) %config(noreplace) %{kolab_webroot}/fbview/kronolith/config/*.xml
%{kolab_webroot}/freebusy/*.php
%{kolab_webroot}/kolabfilter/*.php
%{_datadir}/pear/*
%{_datadir}/pear/.registry/*.reg



