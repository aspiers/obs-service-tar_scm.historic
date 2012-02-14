#!/usr/bin/python

import os
from pprint import pprint, pformat
import re
import tarfile
import unittest

line_start = '(^|\n)'

class TestAssertions(unittest.TestCase):
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

    def assertRanInitialClone(self, logpath, loglines):
        self._find(logpath, loglines, self.initial_clone_command, self.update_cache_command)

    def assertRanUpdate(self, logpath, loglines):
        self._find(logpath, loglines, self.update_cache_command, self.initial_clone_command)

    def _find(self, logpath, loglines, should_find, should_not_find):
        print "####", should_find
        found = False
        regexp = re.compile('^' + should_find)
        for line in loglines:
            msg = \
                "Shouldn't find /%s/ in %s; log was:\n" \
                "----\n%s\n----\n" \
                % (should_not_find, logpath, "".join(loglines))
            self.assertNotRegexpMatches(line, should_not_find, msg)
            if regexp.search(line):
                found = True
        msg = \
            "Didn't find /%s/ in %s; log was:\n" \
            "----\n%s\n----\n" \
            % (regexp.pattern, logpath, "".join(loglines))
        self.assertTrue(found, msg)
