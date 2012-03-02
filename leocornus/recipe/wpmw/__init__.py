# __init__.py

from fnmatch import fnmatch
from zc.buildout.download import Download

import os
import logging


# we will support different format for true.
TRUE_VALUES = ('yes', 'true', '1', 'on')

# recipe class to download and install wordpress plugins.
class Plugins(object):
    """
    download, extract plugins package and create symlink for each 
    plugins
    """

    # constructor
    def __init__(self, buildout, name, options):
        self.options = options
        self.name = name
        self.buildout = buildout

    # install method
    def install(self):

        path = 'testing'
        os.mkdir(path)

        return path

    # update method.
    def update(self):

        pass
