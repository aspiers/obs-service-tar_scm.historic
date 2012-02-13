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

