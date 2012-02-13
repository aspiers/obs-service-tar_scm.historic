#!/usr/bin/python

import sys
import unittest

from gittests import GitTests
from svntests import SvnTests
from hgtests  import HgTests
from bzrtests import BzrTests

if __name__ == '__main__':
    #unittest.main()
    #unittest.main(buffer=True)

    suite = unittest.TestSuite()
    testclasses = [
        SvnTests,
        GitTests,
        HgTests,
        BzrTests,
    ]
    for testclass in testclasses:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(testclass))

    runner_args = {
        'buffer' : True,
        #'verbosity' : 2,
        'failfast': True,
    }
    runner = unittest.TextTestRunner(**runner_args)
    result = runner.run(suite)

    if result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)
