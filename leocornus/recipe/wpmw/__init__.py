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

        # set up the default download cache folder.
        buildout['buildout'].setdefault(
            'download-cache',
            os.path.join(buildout['buildout']['directory'], 'downloads'))

        # set up default if it is necessary.
        options.setdefault('plugins-repo', 'http://downloads.wordpress.org/plugin')
        options.setdefault('ignore-existing', 'true');
        # get a list of plugins.
        self.plugins = [plugin.strip().split('=') for plugin in options.get('plugins', '').strip().splitlines() if plugin.strip()]

    # install method
    def install(self):

        log = logging.getLogger(self.name)

        # the zc.buildout download facility will save everything in download
        # cache.  We need make sure it is exist.
        if not os.path.exists(self.buildout['buildout']['download-cache']):
            os.makedirs(self.buildout['buildout']['download-cache'])

        # get a zc.buildout download instance
        download = Download(self.buildout['buildout'])

        parts = []

        # process the plugins one by one.
        for pId, pVersion in self.plugins:
            # the download url.
            url = self.options.get('plugins-repo') + '/' + pId + '.' + pVersion + '.zip'
            path, is_temp = download(url)

            # destination is parts/plugins/PLUGIN_ID-PLUGIN_VERSION
            dest = os.path.join(self.buildout['buildout']['parts-directory'], 
                                'plugins', pId + '-' + pVersion)
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

            shutil.rmtree(extract_dir)

        return parts

    # update method.
    def update(self):

        pass
