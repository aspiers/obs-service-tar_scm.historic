#!/usr/bin/python

from   unittest    import expectedFailure

from   commontests import CommonTests
from   bzrfixtures import BzrFixtures
from   utils       import run_bzr

class BzrTests(CommonTests):
    scm = 'bzr'
    initial_clone_command = 'bzr checkout'
    update_cache_command  = 'bzr update'
    fixtures_class = BzrFixtures

    def default_version(self):
        return self.rev(2)

