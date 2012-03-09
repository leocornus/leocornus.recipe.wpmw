# __init__.py

from fnmatch import fnmatch
from zc.buildout.download import Download

import os
import logging
import setuptools.archive_util
import shutil
import tempfile
import zc.buildout


# we will support different format for true.
TRUE_VALUES = ('yes', 'true', '1', 'on')

# the base class for all recipes.
class Base:
    """
    The base class will offer the general funtions.
    """
    
    # constructor
    def __init__(self, buildout, name, options):

        self.options = options
        # the part's name.
        self.name = name
        self.buildout = buildout

        # set up the default download cache folder.
        buildout['buildout'].setdefault(
            'download-cache',
            os.path.join(buildout['buildout']['directory'], 'downloads'))

        # set up default for ignore-existing. 
        options.setdefault('ignore-existing', 'true');

    # download, extract, and symlink
    def downloadExtract(self, targetFolder, srcRepo, srcList):
        """
        download all sources in srcList, extract them and create symlink in target
        folder.  all sources will be saved in folder parts/PART-NAME. Each source is saved
        in srcList as the following format: (id, version).
        """

        log = logging.getLogger(self.name)

        # the zc.buildout download facility will save everything in download
        # cache.  We need make sure it is exist.
        if not os.path.exists(self.buildout['buildout']['download-cache']):
            os.makedirs(self.buildout['buildout']['download-cache'])

        # get a zc.buildout download instance
        download = Download(self.buildout['buildout'])

        parts = []
        # add the base directory name to parts, so it will be removed during
        # uninstalling.
        partdir = os.path.join(self.buildout['buildout']['parts-directory'],
                               self.name)
        parts.append(partdir)

        # process the sources one by one.
        for srcId, srcVersion in srcList:
            # the download url.
            url = srcRepo + '/' + srcId + '.' + srcVersion + '.zip'
            path, is_temp = download(url)

            # destination is parts/PART-NAME/PLUGIN_ID-PLUGIN_VERSION
            dest = os.path.join(self.buildout['buildout']['parts-directory'], 
                                self.name, srcId + '-' + srcVersion)
            if not os.path.isdir(dest):
                os.makedirs(dest)
                parts.append(dest)

            # Extract the package
            extract_dir = tempfile.mkdtemp("buildout-" + self.name)
            try:
                setuptools.archive_util.unpack_archive(path, extract_dir)
            except setuptools.archive_util.UnrecognizedFormat:
                log.error('Unable to extract the package %s. Unknown format.', path)
                raise zc.buildout.UserError('Package extraction error')

            top_level_contents = os.listdir(extract_dir)
            if len(top_level_contents) != 1:
                log.error('Unable to strip top level directory because there are more '
                          'than one element in the root of the package.')
                raise zc.buildout.UserError('Invalid package contents')
            base = os.path.join(extract_dir, top_level_contents[0])

            log.info('Extracting package to %s' % dest)

            ignore_existing = self.options['ignore-existing'].strip().lower() in TRUE_VALUES
            for filename in os.listdir(base):
                filenameDest = os.path.join(dest, filename)
                if os.path.exists(filenameDest):
                    if ignore_existing:
                        log.info('Ignoring existing target: %s' % filenameDest)
                    else:
                        log.error('Target %s already exists. Either remove it or set '
                                  '``ignore-existing = true`` in your buildout.cfg to ignore existing '
                                  'files and directories.', filenameDest)
                        raise zc.buildout.UserError('File or directory already exists.')
                else:
                    # Only add the file/directory to the list of installed
                    # parts if it does not already exist. This way it does
                    # not get accidentally removed when uninstalling.
                    parts.append(filenameDest)

                shutil.move(os.path.join(base, filename), filenameDest)

            # create the symlink for this srouce
            linkName = os.path.join(targetFolder, srcId)
            log.info('Create symlink to %s' % linkName)
            if os.path.lexists(linkName):
                os.unlink(linkName)
            os.symlink(dest, linkName)

            shutil.rmtree(extract_dir)

        return parts

# recipe class to download and install wordpress plugins.
class Plugins(Base):
    """
    download, extract plugins package and create symlink for each 
    plugins
    """

    # constructor
    def __init__(self, buildout, name, options):

        # Base constructor
        Base.__init__(self, buildout, name, options)

        # set up default for plugins.
        options.setdefault('plugins-repo', 'http://downloads.wordpress.org/plugin')
        # get a list of plugins.
        self.plugins = [plugin.strip().split('=') for plugin in options.get('plugins', '').strip().splitlines() if plugin.strip()]

    # install method
    def install(self):

        log = logging.getLogger(self.name)

        # the wordpress plugins diretory
        wpPlugins = self.options.get('wordpress-root') + '/wp-content/plugins'

        parts = self.downloadExtract(wpPlugins, self.options.get('plugins-repo'), self.plugins)

        return parts

    # update method.
    def update(self):

        pass

# recipe class to download and install MediaWiki Extensions.
class Extensions(Base):
    """
    download, extract extension packages and create symlink for each 
    extension
    """

    # constructor
    def __init__(self, buildout, name, options):

        # Base constructor
        Base.__init__(self, buildout, name, options)

        # set up default for plugins.
        options.setdefault('extensions-repo', 'http://')
        # get a list of plugins.
        self.extensions = [ext.strip().split('=') for ext in options.get('extensions', '').strip().splitlines() if ext.strip()]

    # install method
    def install(self):

        log = logging.getLogger(self.name)

        # the wordpress plugins diretory
        mwExtensions = self.options.get('mediawiki-root') + '/extensions'

        parts = self.downloadExtract(mwExtensions, self.options.get('extensions-repo'), self.extensions)

        return parts

    # update method.
    def update(self):

        pass

# simple recipe to create symlinks from target folder to link folder.
class Symlinks(object):
    """
    create symlinks for all names from target folder to link folder.
    """

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name

        self.targetFolder = options.get('target-folder')
        self.linkFolder = options.get('link-folder')
        self.names = [name.strip() for name in options.get('names', '').strip().splitlines()]

    def performSymlink(self, targetFolder, linkFolder, names):

        log = logging.getLogger(self.name)

        for name in names:
            linkName = os.path.join(linkFolder, name)
            if os.path.lexists(linkName):
                os.unlink(linkName)

            targetName = os.path.join(targetFolder, name)
            if os.path.exists(targetName):
                log.info('Create symlink to %s' % linkName)
                os.symlink(targetName, linkName)
            else:
                log.info('Target %s not exist, ignoring...' % targetName)

    def install(self):

        self.performSymlink(self.targetFolder, self.linkFolder, self.names) 

        return ''

    def update(self):

        self.performSymlink(self.targetFolder, self.linkFolder, self.names)
