#!/usr/bin/python

import unittest

from gittests import GitTests

if __name__ == '__main__':
    #unittest.main()
    #unittest.main(buffer=True)

    suite = unittest.TestLoader().loadTestsFromTestCase(GitTests)
    runner_args = {
        'buffer' : True,
        #'verbosity' : 2,
    }
    unittest.TextTestRunner(**runner_args).run(suite)
