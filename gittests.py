#!/usr/bin/python

import os
import subprocess
import unittest
import shutil
import sys

from procutils import quietrun
from testsbase import TestsBase

def create_git_commits(start, end):
    subdir = 'subdir'
    if not os.path.exists(subdir):
        os.mkdir(subdir)
    for i in xrange(start, end+1):
        for fn in ('a', subdir + '/b'):
            f = open(fn, 'w')
            f.write(str(i))
            f.close()
        quietrun('git add .')
        quietrun('git commit -m%d' % i)

def run_git(repo, opts):
    return subprocess.check_output('cd %s && git %s' % (repo, opts), shell=True)

class GitTests(TestsBase):
    @classmethod
    def repo_dir(cls):
        return cls.fixtures_dir() + '/repo.git'

    @classmethod
    def repo_url(cls):
        return 'file://' + cls.repo_dir()

    @classmethod
    def setup_fixtures(cls):
        if os.path.exists(cls.fixtures_dir()):
            shutil.rmtree(cls.fixtures_dir())
        os.makedirs(cls.fixtures_dir())

        cls.init_git_repo(cls.repo_dir())

        cls.timestamps   = { }
        cls.sha1s        = { }

        create_git_commits(1, 10)
        cls.record_git_tag('ten')

        create_git_commits(11, 20)
        cls.record_git_tag('twenty')

        create_git_commits(21, 30)
        cls.record_git_tag('thirty')

        cls.reset_upstream('ten')

    @classmethod
    def init_git_repo(cls, repo):
        os.makedirs(repo)
        os.chdir(repo)
        quietrun('git init')
        quietrun('git config user.name test')
        quietrun('git config user.email test@test.com')

    @classmethod
    def record_git_tag(cls, tag):
        quietrun('git tag ' + tag)
        cls.timestamps[tag] = cls.get_git_metadata('%at')
        cls.sha1s[tag]      = cls.get_git_metadata('%h')

    @classmethod
    def get_git_metadata(cls, formatstr):
        return run_git(cls.repo_dir(), 'log -n1 --pretty=format:%s' % formatstr)

    @classmethod
    def reset_upstream(cls, tag):
        run_git(cls.repo_dir(), 'reset --hard %s 2>&1' % tag)

    def stdargs(self, *args):
        return [ '--url', self.repo_url(), '--scm', 'git' ] + list(args)

    def assertPkgWorkingDir(self, name, numcommits, sha1):
        wd = os.path.join(self.pkgdir, name)
        self.assertTrue(os.path.exists(wd), '%s did not exist' % wd)
        self.assertTrue(os.path.isdir(wd),  '%s was not a dir' % wd)

        out = run_git(wd, 'log --pretty=oneline | wc -l')
        self.assertRegexpMatches(out, '^\d+$')
        self.assertEqual(int(out), numcommits)

        out = run_git(wd, 'rev-parse --short HEAD')
        self.assertEqual(out, sha1 + "\n")

    def test_plain(self):
        self.tar_scm_std()
        basename = 'repo-%s' % self.timestamps['ten']
        self.assertTarOnly(basename)

    def test_exclude_git(self):
        self.tar_scm_std('--exclude', '.git')
        basename = 'repo-%s' % self.timestamps['ten']
        self.assertTarOnly(basename)

    def test_subdir(self):
        self.tar_scm_std('--subdir', 'subdir')
        basename = 'repo-%s' % self.timestamps['ten']
        self.assertTarOnly(basename, tarchecker=self.assertSubdirTar)

    def test_filename(self):
        self.tar_scm_std('--filename', 'myfilename')
        basename = 'myfilename-%s' % self.timestamps['ten']
        self.assertTarOnly(basename)

    def test_version(self):
        version = '0.5'
        self.tar_scm_std('--version', version)
        basename = 'repo-%s' % version
        self.assertTarOnly(basename)

    def test_filename_version(self):
        version = '0.6'
        filename = 'myfilename'
        self.tar_scm_std('--filename', filename, '--version', version)
        basename = filename + '-' + version
        self.assertTarOnly(basename)

    # FIXME: currently no way of testing that this did the right
    # thing, because the cloned repo is removed before the source
    # service terminates.  To test this properly, we'd need to wrap or
    # stub the git executable by prepending to $PATH.
    def test_history_depth(self):
        self.tar_scm_std('--history-depth', '1')
        basename = 'repo-%s' % self.timestamps['ten']
        self.assertTarOnly(basename)

    # FIXME: same issue here as above
    def test_history_depth_full(self):
        self.tar_scm_std('--history-depth', 'full')
        basename = 'repo-%s' % self.timestamps['ten']
        self.assertTarOnly(basename)
