# tests.py

import doctest

import os
import re
import shutil
import unittest
import zc.buildout.testing
import zc.buildout.tests

optionflags =  (doctest.ELLIPSIS |
                doctest.NORMALIZE_WHITESPACE)

# set up the buildout testing enviroment.
def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)
    zc.buildout.testing.install_develop('leocornus.recipe.wpmw', test)

def test_suite():

    suite = unittest.TestSuite()

    # add the README.rst
    suite.addTest(
        doctest.DocFileSuite(
            'README.rst',
            setUp=setUp,
            tearDown=zc.buildout.testing.buildoutTearDown,
            optionflags=optionflags,
        ),
    )

    # add the test-wmflabs.rst, 
    # which will testing download from 
    # http://extdist.wmflabs.org/dist/.
    # including both extensions and skins.
    suite.addTest(
        doctest.DocFileSuite(
            'test-wmflabs.rst',
            setUp=setUp,
            tearDown=zc.buildout.testing.buildoutTearDown,
            optionflags=optionflags,
        ),
    )

    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
