%define _enable_debug_packages %{nil}
%define debug_package          %{nil}

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
Release:	10
License:	GPL
Group:		System/Servers
URL:		http://www.kolab.org/
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
%defattr(-,root,root)
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


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 2.1.0-9mdv2011.0
+ Revision: 666035
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 2.1.0-8mdv2011.0
+ Revision: 606268
- rebuild

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 2.1.0-7mdv2010.0
+ Revision: 425491
- rebuild

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 2.1.0-6mdv2009.0
+ Revision: 221908
- rebuild

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Sun Jan 13 2008 Thierry Vignaud <tv@mandriva.org> 2.1.0-5mdv2008.1
+ Revision: 150431
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Sep 10 2007 Oden Eriksson <oeriksson@mandriva.com> 2.1.0-4mdv2008.0
+ Revision: 84127
- use correct directories for resmgr

* Mon Jun 25 2007 Oden Eriksson <oeriksson@mandriva.com> 2.1.0-3mdv2008.0
+ Revision: 43813
- fix deps

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 2.1.0-2mdv2008.0
+ Revision: 33619
- fix permisions

* Sat May 26 2007 Oden Eriksson <oeriksson@mandriva.com> 2.1.0-1mdv2008.0
+ Revision: 31491
- 2.1.0
- fixed a lot of stuff..


* Wed Oct 11 2006 Oden Eriksson <oeriksson@mandriva.com>
+ 2006-10-10 09:51:42 (63285)
- hmmm..., forgot the mkrel macro

* Wed Oct 11 2006 Oden Eriksson <oeriksson@mandriva.com>
+ 2006-10-10 09:48:08 (63283)
- rebuild

* Tue May 30 2006 Andreas Hasenack <andreas@mandriva.com>
+ 2006-05-29 08:36:37 (31646)
- renamed mdv to packages because mdv is too generic and it's hosting only packages anyway

* Sun Sep 11 2005 oeriksson
+ 2005-09-10 07:20:31 (876)
- new snap (small fixes)

* Sat Aug 20 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-08-19 14:50:47 (708)
- don't create user/groups here, leave it to the kolab
  package which we requires(pre) anyway (but see here:
  http://archives.mandrivalinux.com/cooker/2005-08/msg03078.php)
- make /var/spool/resmgr mode 0700 since it stores temporary
  mail messages that are being scanned

* Fri Aug 19 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-08-18 13:30:06 (699)
- added phpself patch: $PHP_SELF -> $_SERVER['PHP_SELF']

* Fri Aug 19 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-08-18 10:53:05 (694)
- added php-pear-Date and php-pear-HTTP_Request requirements
  (needed by fbview)
- added fbviewroot patch to fix url (/fbview -> /kolab/fbview)

* Wed Aug 17 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-08-16 09:21:39 (666)
- changed freebusy directory ownership to root:root (instead
  of apache:apache). Apache doesn't need to write there.

* Wed Aug 17 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-08-16 09:17:43 (665)
- made cache and locks subdirectories under freebusy mode
  0770 instead of 0777 (it's apache who is writing there, and
  it already owns these dirs)

* Wed Aug 17 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-08-16 09:15:01 (664)
- added requirement for php-dba, used by freebusy

* Wed Aug 17 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-08-16 07:25:19 (658)
- first stab at a patch to make freebusy use php-dom instead
  of php-domxml which is no longer available for php5

* Tue Aug 16 2005 oeriksson
+ 2005-08-15 07:02:27 (644)
- fix kolab-server/kolab renaming

* Tue Aug 16 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-08-15 03:15:35 (635)
- added a missing %%{buildroot} (I'm glad we don't need to build
  packages as root ;) )

* Sun Aug 14 2005 oeriksson
+ 2005-08-13 04:35:20 (626)
- fix smarter perl search and replace (works faster)
- fix config files if needed for the horde stuff
- fix deps and file permissions as per docs
- add the kolab user and group from here because i never managed to
  make urpmi install kolab-server first...
- nuke some left over files with bad extensions (dupes)

* Sat Aug 13 2005 oeriksson
+ 2005-08-12 01:41:51 (608)
- fix some paths

* Fri Aug 12 2005 oeriksson
+ 2005-08-11 09:02:11 (604)
- merge in the new snap version

* Fri Aug 12 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-08-11 08:55:43 (602)
- fixed another hardcoded path

* Thu Aug 11 2005 oeriksson
+ 2005-08-10 22:57:01 (589)
- fix the path to /var/resmgr/*.log
- nuke the %%{_sysconfdir}/kolab/resmgr stuff, it's now moved
  to the kolab-server package

* Tue Aug 09 2005 oeriksson
+ 2005-08-08 01:56:47 (551)
- new snap (20050807), some files in the previous tar ball was incorrect

* Tue Aug 09 2005 oeriksson
+ 2005-08-08 01:54:44 (549)
- new snap (20050807), some files in the previous tar ball was incorrect
- use one user only, not kolab-r and kolab-n
- %%undefine __find_provides and %%undefine __find_requires for now
- added Requires(pre): kolab-server >= 1.9.5 to make urpmi
  kolab-server install the kolab-x packages in the correct order
- fix attribs for the %%{kolab_webroot}/freebusy/cache and
  %%{kolab_webroot}/locks directories

* Sat Aug 06 2005 Andreas Hasenack <andreas@mandriva.com>
+ 2005-08-05 10:23:46 (543)
- removed another hardcoded path (and replaced it by a new
  hardcoded path, duh)

* Tue Aug 02 2005 oeriksson
+ 2005-08-01 14:49:04 (493)
- fix another stupid deps problem...

* Tue Aug 02 2005 oeriksson
+ 2005-08-01 14:38:45 (492)
- fix the apache config

* Tue Aug 02 2005 oeriksson
+ 2005-08-01 08:36:33 (488)
- added a dependenciy on php-mcal, seems required by the kronolith horde stuff...

* Tue Aug 02 2005 oeriksson
+ 2005-08-01 08:26:26 (486)
- use a recent CVS snapshot (20050801)
- fix deps

* Fri Jul 29 2005 oeriksson
+ 2005-07-28 02:16:56 (453)
- initial Mandriva package

