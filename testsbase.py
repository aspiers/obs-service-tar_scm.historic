#!/usr/bin/python

import os
import shutil
import tarfile
import unittest
from pprint import pprint, pformat
from procutils import shexec, run_cmd

class TestsBase(unittest.TestCase):
    @classmethod
    def _tests_dir(cls):
        return os.path.abspath(os.path.dirname(__file__)) # os.getcwd()

    @classmethod
    def tmpdir(cls):
        return cls._tests_dir() + '/tmp'

    @classmethod
    def fixtures_dir(cls):
        return cls.tmpdir() + '/fixtures'

    @classmethod
    def tar_scm_bin(cls):
        tar_scm = cls._tests_dir() + '/tar_scm'
        if not os.access(tar_scm, os.X_OK):
            raise RuntimeError, "Failed to find tar_scm at " + tar_scm
        return tar_scm

    @classmethod
    def setUpClass(cls):
        cls.setup_fixtures()

    def mkfreshdir(self, d):
        if d.find('/tmp/') == -1:
            raise RuntimeError, 'unsafe call: mkfreshdir(%s)' % d

        cwd = os.getcwd()
        os.chdir('/')
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d)
        os.chdir(cwd)

    def calcPaths(self):
        self.testname = self._testMethodName
        self.test_dir = os.path.join(self.tmpdir(), self.testname)
        self.pkgdir   = os.path.join(self.test_dir, 'pkg')
        self.outdir   = os.path.join(self.test_dir, 'out')

    def setUp(self):
        self.calcPaths()
        self.initDirs()

        # osc launches source services with cwd as pkg dir
        os.chdir(self.pkgdir)

    def initDirs(self):
        # pkgdir persists between tests (although a test can invoke mkfreshdir)
        if not os.path.exists(self.pkgdir):
            os.makedirs(self.pkgdir)

    def tearDown(self):
        self.postRun()

    def postRun(self):
        # Simulate osc copying files from temporary --outdir back to
        # package source directory, so our tests can catch any
        # potential side-effects due to the persistent nature of the
        # package source directory.

        self.service = { 'mode' : 'disabled' }
        temp_dir = self.outdir
        dir = self.pkgdir
        service = self.service

        # This code copied straight out of osc/core.py Serviceinfo.execute()
        if service['mode'] == "disabled" or service['mode'] == "trylocal" or service['mode'] == "localonly" or callmode == "local" or callmode == "trylocal":
            for filename in os.listdir(temp_dir):
                shutil.move( os.path.join(temp_dir, filename), os.path.join(dir, filename) )
        else:
            for filename in os.listdir(temp_dir):
                shutil.move( os.path.join(temp_dir, filename), os.path.join(dir, "_service:"+name+":"+filename) )
                
        self.reset_upstream('ten')

    def assertNumDirents(self, dir, expected, msg = ''):
        dirents = os.listdir(dir)
        got = len(dirents)
        if len(msg) > 0: msg += "\n"
        msg += 'expected %d file(s), got %d: %s' % (expected, got, pformat(dirents))
        self.assertEqual(expected, got, msg)
        return dirents

    def assertNumTarEnts(self, tar, expected, msg = ''):
        self.assertTrue(tarfile.is_tarfile(tar))
        th = tarfile.open(tar)
        tarents = th.getmembers()
        got = len(tarents)
        if len(msg) > 0: msg += "\n"
        msg += 'expected %s to have %d entries, got %d:\n%s' % \
            (tar, expected, got, pformat(tarents))
        self.assertEqual(expected, got, msg)
        return th, tarents

    def assertStandardTar(self, tar, top):
        th, entries = self.assertNumTarEnts(tar, 4)
        pprint(entries)
        self.assertEqual(entries[0].name, top)
        self.assertEqual(entries[1].name, top + '/a')
        self.assertEqual(entries[2].name, top + '/subdir')
        self.assertEqual(entries[3].name, top + '/subdir/b')
        return th

    def assertSubdirTar(self, tar, top):
        th, entries = self.assertNumTarEnts(tar, 2)
        self.assertEqual(entries[0].name, top)
        self.assertEqual(entries[1].name, top + '/b')
        return th

    def checkTar(self, tar, tarbasename, toptardir=None, tarchecker=None):
        if not toptardir:
            toptardir = tarbasename
        if not tarchecker:
            tarchecker = self.assertStandardTar

        self.assertEqual(tar, '%s.tar' % tarbasename)
        tarpath = os.path.join(self.outdir, tar)
        return tarchecker(tarpath, toptardir)

    def assertTarOnly(self, tarbasename, **kwargs):
        dirents = self.assertNumDirents(self.outdir, 1)
        return self.checkTar(dirents[0], tarbasename, **kwargs)

    def assertTarAndDir(self, tarbasename, dirname=None, **kwargs):
        if not dirname:
            dirname = tarbasename

        dirents = self.assertNumDirents(self.outdir, 2)
        pprint(dirents)

        if dirents[0][-4:] == '.tar':
            tar = dirents[0]
            wd  = dirents[1]
        elif dirents[1][-4:] == '.tar':
            tar = dirents[1]
            wd  = dirents[0]
        else:
            self.fail('no .tar found in ' + self.outdir)

        self.assertEqual(wd, dirname)
        self.assertTrue(os.path.isdir(os.path.join(self.outdir, wd)),
                        dirname + ' should be directory')

        return self.checkTar(tar, tarbasename, **kwargs)

    def assertTarMemberContains(self, th, tarmember, contents):
        f = th.extractfile(tarmember)
        self.assertEqual(contents, "\n".join(f.readlines()))

    def tar_scm_std(self, *args, **kwargs):
        return self.tar_scm(self.stdargs(*args), **kwargs)

    def tar_scm_std_fail(self, *args):
        return self.tar_scm(self.stdargs(*args), should_succeed=False)

    def tar_scm(self, args, should_succeed=True):
        # simulate new temporary outdir for each tar_scm invocation
        self.mkfreshdir(self.outdir)
        cmd = [ self.tar_scm_bin() ] + args + [ '--outdir', self.outdir ]
        cmdstr = " ".join(cmd) + " 2>&1"
        print "\n"
        print "-" * 70
        print "Running", cmdstr
        print "Output:"
        print "------"
        (stdout, stderr, ret) = run_cmd(cmdstr)
        print stdout,
        # print "------"
        # print stderr,
        print "------"
        succeeded = ret == 0
        self.assertEqual(succeeded, should_succeed)
        return (stdout, stderr, ret)
