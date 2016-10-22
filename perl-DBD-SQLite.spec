%{?scl:%scl_package perl-DBD-SQLite}

Name:           %{?scl_prefix}perl-DBD-SQLite
Version:        1.50
Release:        4%{?dist}
Summary:        SQLite DBI Driver
Group:          Development/Libraries
License:        (GPL+ or Artistic) and Public Domain
URL:            http://search.cpan.org/dist/DBD-SQLite/
Source0:        http://search.cpan.org/CPAN/authors/id/I/IS/ISHIGAKI/DBD-SQLite-%{version}.tar.gz
Patch0:         perl-DBD-SQLite-bz543982.patch
# Remove notes about bundled sqlite C source from man page and README
Patch1:         DBD-SQLite-1.50-Remove-bundled-source-extentions.patch
# Adjust to sqlite-3.11.0, bug #1309675, in upstream after 1.50
Patch2:         DBD-SQLite-1.50-two-arg-fts3_tokenizer-is-disabled-by-default-for-se.patch
# Adjust to sqlite-3.11.0, bug #1309675, in upstream after 1.50
Patch3:         DBD-SQLite-1.50-register-perl-tokenizer-only-if-DBD-SQLite-is-compil.patch
# Adjust to sqlite-3.11.0, bug #1309675, in upstream after 1.50
Patch4:         DBD-SQLite-1.50-see-if-SQLITE_ENABLE_FTS3_TOKENIZER-environmental-va.patch
# if sqlite >= 3.1.3 then
#   perl-DBD-SQLite uses the external library
# else
#   perl-DBD-SQLite is self-contained (uses the sqlite local copy)
BuildRequires:  sqlite-devel
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  %{?scl_prefix}perl
BuildRequires:  %{?scl_prefix}perl-devel
BuildRequires:  %{?scl_prefix}perl-generators
BuildRequires:  %{?scl_prefix}perl(base)
BuildRequires:  %{?scl_prefix}perl(Config)
BuildRequires:  %{?scl_prefix}perl(constant)
# Prevent bug #443495
BuildRequires:  %{?scl_prefix}perl(DBI) >= 1.607
BuildRequires:  %{?scl_prefix}perl(DynaLoader)
BuildRequires:  %{?scl_prefix}perl(ExtUtils::MakeMaker)
BuildRequires:  %{?scl_prefix}perl(File::Spec) >= 0.82
BuildRequires:  %{?scl_prefix}perl(Scalar::Util)
BuildRequires:  %{?scl_prefix}perl(strict)
BuildRequires:  %{?scl_prefix}perl(Tie::Hash)
BuildRequires:  %{?scl_prefix}perl(warnings)
BuildRequires:  sed
# Tests only
BuildRequires:  %{?scl_prefix}perl(bytes)
BuildRequires:  %{?scl_prefix}perl(Carp)
BuildRequires:  %{?scl_prefix}perl(Data::Dumper)
BuildRequires:  %{?scl_prefix}perl(Encode)
BuildRequires:  %{?scl_prefix}perl(Exporter)
BuildRequires:  %{?scl_prefix}perl(File::Spec::Functions)
BuildRequires:  %{?scl_prefix}perl(File::Temp)
BuildRequires:  %{?scl_prefix}perl(FindBin)
BuildRequires:  %{?scl_prefix}perl(lib)
BuildRequires:  %{?scl_prefix}perl(locale)
BuildRequires:  %{?scl_prefix}perl(Test::Builder)
BuildRequires:  %{?scl_prefix}perl(Test::More) >= 0.42
BuildRequires:  %{?scl_prefix}perl(Unicode::UCD)
BuildRequires:  %{?scl_prefix}perl(vars)
Requires:       %{?scl_prefix}perl(:MODULE_COMPAT_%(%{?scl:scl enable %{scl} '}eval "$(perl -V:version)";echo $version%{?scl:'}))

%{?perl_default_filter}

%description
SQLite is a public domain RDBMS database engine that you can find at
http://www.hwaci.com/sw/sqlite/.

This module provides a SQLite RDBMS module that uses the system SQLite 
libraries.

%prep
%setup -q -n DBD-SQLite-%{version}
%patch0 -p1 -b .bz543982
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
# Remove bundled sqlite libraries (BZ#1059154)
# System libraries will be used
rm sqlite*
sed -i -e '/^sqlite/ d' MANIFEST

%build
CFLAGS="%{optflags}" %{?scl:scl enable %{scl} '}perl Makefile.PL INSTALLDIRS=vendor && make %{?_smp_mflags} OPTIMIZE="%{optflags}"%{?scl:'}

%install
%{?scl:scl enable %{scl} '}make pure_install DESTDIR=%{buildroot}%{?scl:'}
find %{buildroot} -type f \( -name .packlist -o \
     -name '*.bs' -size 0 \) -exec rm -f {} ';'
%{_fixperms} %{buildroot}/*

%check
%{?scl:scl enable %{scl} '}make test%{?scl:'}

%files
%doc Changes README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/DBD/
%{_mandir}/man3/*.3pm*

%changelog
* Tue Jul 12 2016 Petr Pisar <ppisar@redhat.com> - 1.50-4
- SCL

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.50-3
- Perl 5.24 rebuild

* Thu Feb 18 2016 Petr Pisar <ppisar@redhat.com> - 1.50-2
- Adjust to sqlite-3.11.0 (bug #1309675)
- Rebase Remove-bundled-source-extentions.patch to prevent from packing backup
  files

* Thu Feb 11 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.50-1
- 1.50 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.48-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Petr Pisar <ppisar@redhat.com> - 1.48-3
- Adapt to sqlite-3.10.0 by adding DBD::SQLite::strlike() (bug #1298628)

* Fri Jun 19 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.48-2
- Updated patch

* Thu Jun 18 2015 Tom Callaway <spot@fedoraproject.org> - 1.48-1
- update to 1.48

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.46-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.46-3
- Perl 5.22 rebuild

* Fri Mar 20 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.46-2
- Correct license from (GPL+ or Artistic) to ((GPL+ or Artistic) and
  Public Domain)

* Wed Dec 10 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.46-1
- 1.46 bump

* Wed Oct 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.44-1
- 1.44 bump

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.42-5
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.42-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 15 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.42-3
- Removed bundled sqlite library and updated man page (BZ#1059154)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 20 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.42-1
- 1.42 bump

* Wed Jan 29 2014 Petr Pisar <ppisar@redhat.com> - 1.40-3
- Fix tests with sqlite >= 3.8.2 (bug #1058709)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.40-1
- 1.40 bump

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 1.39-2
- Perl 5.18 rebuild

* Mon Jun 10 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.39-1
- 1.39 bump
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Update source URL

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.37-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.37-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 16 2012 Petr Pisar <ppisar@redhat.com> - 1.37-2
- Perl 5.16 rebuild

* Tue Jun 12 2012 Petr Šabata <contyk@redhat.com> - 1.37-1
- 1.37 bump (sqlite3.7.11 and various bugfixes)
- Drop command macros
- Fix dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 29 2011 Petr Šabata <contyk@redhat.com> - 1.35-1
- 1.35 bump

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.33-2
- Perl mass rebuild

* Mon May 30 2011 Petr Sabata <contyk@redhat.com> - 1.33-1
- 1.33 bump
- BuildRoot and defattr cleanup
- Dropping the FTS3 tests patch; included upstream

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 1.31-2
- Rebuilt for gcc bug 634757

* Wed Sep 15 2010 Petr Sabata <psabata@redhat.com> - 1.31-1
- New release, v1.31
- Significant FTS3 changes -- might break compatibility with pre-1.30 applications using FTS3
- New FTS3 tests patch by Paul Howarth

* Tue Aug 24 2010 Adam Tkac <atkac redhat com> - 1.29-4
- fix testsuite to run with the latest sqlite (bugs.debian.org/591111)

* Tue Aug 24 2010 Adam Tkac <atkac redhat com> - 1.29-3
- rebuild

* Mon Jun 28 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.29-2
- fix description/summary

* Thu Jun 10 2010 Petr Sabata <psabata@redhat.com> - 1.29-1
- Update to the latest release

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.27-4
- Mass rebuild with perl-5.12.0

* Mon Jan 11 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.27-3
- 543982 change Makefile.PL to compile with system sqlite

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.27-2
- rebuild against perl 5.10.1

* Wed Nov 25 2009 Stepan Kasal <skasal@redhat.com> 1.27-1
- new upstream version

* Fri Sep 11 2009 Chris Weyl <cweyl@alumni.drew.edu> - 1.25-4
- Filtering errant private provides

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 10 2009 Stepan Kasal <skasal@redhat.com> 1.25-2
- rebuild against DBI 1.609

* Fri May 29 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.25-1
- 1.25 needed for DBIx::Class 0.08103
- auto-update to 1.25 (by cpan-spec-update 0.01)
- added a new br on perl(File::Spec) (version 0.82)
- altered br on perl(Test::More) (0 => 0.42)
- added a new br on perl(DBI) (version 1.57)

* Mon Apr 20 2009 Marcela Maslanova <mmaslano@redhat.com> 1.23-1
- update to the latest version

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jun  2 2008 Marcela Maslanova <mmaslano@redhat.com> 1.14-8

* Wed Mar 19 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.14-7
- reenable tests

* Tue Mar 18 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.14-6
- apply sanity patches derived from RT#32100

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.14-5.1
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.14-4.1
- Autorebuild for GCC 4.3

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.14-3.1
- tests disabled, due to x86_64 failures

* Tue Jan 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.14-3
- rebuild for new perl

* Wed Dec 19 2007 Steven Pritchard <steve@kspei.com> 1.14-2
- Fix find option order.
- Use fixperms macro instead of our own chmod incantation.

* Mon Dec 10 2007 Robin Norwood <rnorwood@redhat.com> - 1.14-1
- Update to latest upstream version: 1.14
- Remove patch - no longer needed.

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.12-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Thu Sep 14 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.12-2
- Rebuild for FC6.

* Tue Apr 11 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.12-1
- Update to 1.12.

* Wed Apr  5 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.11-4
- Patch to build with system sqlite 3.3.x (#183530).
- Patch to avoid type information segv (#187873).

* Thu Mar  9 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.11-3
- DBD::SQLite fails to build with the current FC-5 sqlite version (3.3.3);
  see bugzilla entry #183530.
  Forcing package rebuild with the included version of sqlite (3.2.7).

* Sat Feb 18 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.11-2
- Rebuild for FC5 (perl 5.8.8).

* Fri Dec  2 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.11-1
- Update to 1.11.

* Fri Dec  2 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.10-1
- Update to 1.10.

* Fri Jul 29 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.09-2
- Build requirement added: sqlite-devel.
- Doc file added: Changes.

* Fri Jul 29 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.09-1
- Update to 1.09.
- This new version can use an external SQLite library (>= 3.1.3).

* Sun Jun 12 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.08-2
- temporary maintainership.

* Sat Jun 11 2005 Michael A. Peters <mpeters@mac.com> 1.08-1.1
- minor changes for initial cvs checkin (removed tabs, better url in
- url tag and description tag)

* Tue Apr 12 2005 Michael A. Peters <mpeters@mac.com> 1.08-1
- created initial spec file from Fedora spectemplate-perl.spec
