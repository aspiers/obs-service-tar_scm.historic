#!/usr/bin/python

import os

from   fixtures  import Fixtures
from   utils     import mkfreshdir, quietrun, run_svn

class SvnFixtures(Fixtures):
    def init(self):
        self.wd_path = self.container_dir + '/wd'

        self.create_repo()
        self.checkout_repo()

        self.added        = { }
        self.timestamps   = { }

        self.create_commits(2)

    def run(self, cmd):
        return run_svn(self.wd_path, cmd)

    def create_repo(self):
        quietrun('svnadmin create ' + self.repo_path)
        print "created repo", self.repo_path

    def checkout_repo(self):
        mkfreshdir(self.wd_path)
        quietrun('svn checkout %s %s' % (self.repo_url, self.wd_path))
        self.wd = self.wd_path


    def do_commit(self, newly_created):
        for new in newly_created:
            if not new in self.added:
                self.run('add ' + new)
                self.added[new] = True
        self.run('commit -m%d' % self.next_commit_rev)

    def get_metadata(self, formatstr):
        return self.run('log -n1' % formatstr)[0]

    def record_rev(self, rev_num):
        self.revs[rev_num] = str(rev_num)
