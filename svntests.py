#!/usr/bin/python

from   unittest    import expectedFailure

from   commontests import CommonTests
from   svnfixtures import SvnFixtures
from   utils       import run_svn

class SvnTests(CommonTests):
    scm = 'svn'
    initial_clone_command = 'svn (co|checkout) '
    update_cache_command  = 'svn up(date)?'
    fixtures_class = SvnFixtures

    def default_version(self):
        return self.rev(2)
