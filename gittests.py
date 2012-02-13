#!/usr/bin/python

import os
import subprocess
from   unittest    import expectedFailure

from   commontests import CommonTests
from   gitfixtures import GitFixtures
from   utils       import run_git

class GitTests(CommonTests):
    scm = 'git'
    initial_clone_command = 'git clone'
    update_cache_command  = 'git fetch'
    fixtures_class = GitFixtures

    def default_version(self):
        return self.timestamps(self.rev(2))

    def test_versionformat_abbrevhash(self):
        self.tar_scm_std('--versionformat', '%h')
        self.assertTarOnly(self.basename(version = self.sha1s(self.rev(2))))

    def test_versionformat_timestamp(self):
        self.tar_scm_std('--versionformat', '%at')
        self.assertTarOnly(self.basename(version = self.timestamps(self.rev(2))))

    def test_versionformat_mixed(self):
        self.tar_scm_std('--versionformat', '%at.master.%h')
        version = '%s.master.%s' % (self.timestamps(self.rev(2)), self.sha1s(self.rev(2)))
        self.assertTarOnly(self.basename(version = version))

    def test_version_versionformat(self):
        self.tar_scm_std('--version', '3.0', '--versionformat', '%at.master.%h')
        version = '%s.master.%s' % (self.timestamps(self.rev(2)), self.sha1s(self.rev(2)))
        self.assertTarOnly(self.basename(version=version))

    def test_versionformat_revision(self):
        self.fixtures.create_commits(4)
        self.tar_scm_std('--versionformat', '%h', '--revision', self.rev(2))
        basename = self.basename(version = self.sha1s(self.rev(2)))
        th = self.assertTarOnly(basename)
        self.assertTarMemberContains(th, basename + '/a', '2')

