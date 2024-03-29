#
# spec file for package obs-service-tar_scm
#
# Copyright (c) 2012 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


%define service tar_scm

Name:           obs-service-%{service}
Summary:        An OBS source service: checkout or update a tar ball from svn/git/hg
License:        GPL-2.0+
Group:          Development/Tools/Building
Url:            https://build.opensuse.org/package/show?package=obs-service-%{service}&project=openSUSE%3ATools
Version:        0.2.3
Release:        0
Source:         %{service}
Source1:        %{service}.service
Source2:        %{service}.rc

# test suite files
Source100:      bzrfixtures.py
Source101:      bzrtests.py
Source102:      commontests.py
Source103:      fixtures.py
Source104:      gitfixtures.py
Source105:      githgtests.py
Source106:      gittests.py
Source107:      hgfixtures.py
Source108:      hgtests.py
Source109:      scmlogs.py
Source110:      svnfixtures.py
Source111:      svntests.py
Source112:      testassertions.py
Source113:      testenv.py
Source114:      test.py
Source115:      utils.py
Source116:      scm-wrapper

Requires:       bzr git mercurial subversion
BuildRequires:  bzr
BuildRequires:  git
BuildRequires:  mercurial
BuildRequires:  python >= 2.6
BuildRequires:  subversion
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
This is a source service for openSUSE Build Service.

It supports downloading from svn, git, hg and bzr repositories.


%prep
%setup -q -D -T 0 -n .

%build

%install
mkdir -p $RPM_BUILD_ROOT/usr/lib/obs/service
install -m 0755 %{SOURCE0} $RPM_BUILD_ROOT/usr/lib/obs/service
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT/usr/lib/obs/service

mkdir -p $RPM_BUILD_ROOT/etc/obs/services
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT/etc/obs/services/%{service}

%check
chmod +x $RPM_SOURCE_DIR/scm-wrapper
: Running the test suite.  Please be patient - this takes a few minutes ...
python $RPM_SOURCE_DIR/test.py

%files
%defattr(-,root,root)
%dir /usr/lib/obs
/usr/lib/obs/service
%dir /etc/obs
%dir /etc/obs/services
%config(noreplace) /etc/obs/services/*

%changelog
