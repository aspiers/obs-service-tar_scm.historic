#!/usr/bin/python

from   commontests import CommonTests
from   hgfixtures import HgFixtures
from   utils       import run_hg

class HgTests(CommonTests):
    scm = 'hg'
    initial_clone_command = 'hg clone'
    update_cache_command  = 'hg pull'
    fixtures_class = HgFixtures

    def default_version(self):
        return self.rev(2)
