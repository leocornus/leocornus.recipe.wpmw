
This recipe should have 2 major functions: WordPress Plugins and 
MediaWiki Extensions

Options
=======

The ``leocornus.recipe.wpmw:Plugins`` recipe could be used to download WordPress
Plugins package, extract to certain folder, and create the symlink to WordPress
wp-content/plugins folder.  It supports the following general options:

Options for all recipes:

``ignore-existing``

    Default is true, ignore existing folder.

Options for ``deploy`` recipe:

``packages``

    A list of packages id and version at format id=version.
    e.g. SomeSkin=1.1

``packages-repo``

    The base URL, where we could download the packages.

``file-extension``

    set the file extension for each package. default is **.zip**

``separator``

    set the separator between name and version. default is **.**.

``destination``

    The target folder where the packages are extracted to.

``action``

    There are 2 values for this option: ``symlink`` and ``copy``.
    Default value is ``symlink``.  This option will be 
    ignored for ``symlink`` and ``download`` recipes.  

Options for ``symlink`` recipe:

``target-folder``

    the target folder, from which we create symlink to the link_name.

``link-folder``

    the link folder will have all the link names.

``names``

    the names used to create the symlink.  The following command will be used:
    $ ln -s target_folder/name link_folder/name

zc.buildout built in a set of easy to use functions to simplfy the testing for buildout
recipe.  Check http://pypi.python.org/pypi/zc.buildout/1.5.2#testing-support for more
details.

Examples for deploy recipe
==========================

Prepare the testing server for download

    >>> import os.path
    >>> testdir = join(os.path.dirname(__file__), 'testdata')
    >>> server = start_server(testdir)

Get ready the testing folders.

    >>> dest = tmpdir('dest')
    >>> mkdir(dest, 'extensions')
    >>> mkdir(dest, 'plugins')
    >>> ls(dest)
    d  extensions
    d  plugins

try to crate a symlink in plugins folder to test the unlink function.

    >>> import os
    >>> bp = tmpdir('bp-fake')
    >>> print bp
    /tmp/.../bp-fake
    >>> os.symlink(bp, os.path.join(dest, 'plugins', 'buddypress'))
    >>> ls(dest, 'plugins')
    d  buddypress

create a broken symlink, we have to use ``os.path.lexists`` to check the link name exist or
not.

    >>> bplink = tmpdir('bp-link')
    >>> os.symlink(bplink, os.path.join(dest, 'plugins', 'buddypress-links'))
    >>> ls(dest, 'plugins')
    d  buddypress
    d  buddypress-links
    >>> remove(bplink)
    >>> ls(dest, 'plugins')
    d  buddypress
    l  buddypress-links

Buildout file to testing deployment with default symlink action.

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts = 
    ...     wpplugins
    ...     mwextensions
    ... 
    ... [wpplugins]
    ... recipe = leocornus.recipe.wpmw:deploy
    ... packages = 
    ...     buddypress=1.5.1
    ...     bp-moderation=0.1.4
    ...     buddypress-links=0.5
    ... packages-repo = http://downloads.wordpress.org/plugin
    ... destination = %(dest)s/plugins
    ...
    ... [mwextensions]
    ... recipe = leocornus.recipe.wpmw:deploy
    ... packages = 
    ...     Cite=r37577
    ...     SemanticForms=1.9.1
    ...     SemanticMediaWiki=1.5.1
    ... packages-repo = %(server)srepos
    ... destination = %(dest)s/extensions
    ... """ % dict(server=server, dest=dest))

Run the buildout

    >>> print system(buildout)
    Installing wpplugins.
    Downloading http://downloads.wordpress.org/plugin/buddypress.1.5.1.zip
    wpplugins: Extracting package to .../sample-buildout/parts/wpplugins/buddypress-1.5.1
    wpplugins: Create symlink to .../dest/plugins/buddypress
    Downloading http://downloads.wordpress.org/plugin/bp-moderation.0.1.4.zip
    wpplugins: Extracting package to .../sample-buildout/parts/wpplugins/bp-moderation-0.1.4
    wpplugins: Create symlink to .../dest/plugins/bp-moderation
    Downloading http://downloads.wordpress.org/plugin/buddypress-links.0.5.zip
    wpplugins: Extracting package to .../sample-buildout/parts/wpplugins/buddypress-links-0.5
    wpplugins: Create symlink to .../dest/plugins/buddypress-links
    Installing mwextensions.
    Downloading http://.../repos/Cite.r37577.zip
    mwextensions: Extracting package to .../sample-buildout/parts/mwextensions/Cite-r37577
    mwextensions: Create symlink to .../dest/extensions/Cite
    Downloading http://.../repos/SemanticForms.1.9.1.zip
    mwextensions: Extracting package to .../sample-buildout/parts/mwextensions/SemanticForms-1.9.1
    mwextensions: Create symlink to .../dest/extensions/SemanticForms
    Downloading http://.../repos/SemanticMediaWiki.1.5.1.zip
    mwextensions: Extracting package to .../sample-buildout/parts/mwextensions/SemanticMediaWiki-1.5.1
    mwextensions: Create symlink to .../dest/extensions/SemanticMediaWiki
    ...

Check the destnation folder

    >>> ls(dest, 'plugins')
    d  bp-moderation
    d  buddypress
    d  buddypress-links
    >>> ls(dest, 'extensions')
    d  Cite
    d  SemanticForms
    d  SemanticMediaWiki

Now, let's try the hard copy action.

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts = 
    ...     wpplugins
    ...     mwextensions
    ... 
    ... [wpplugins]
    ... recipe = leocornus.recipe.wpmw:deploy
    ... action = copy
    ... packages = 
    ...     buddypress=1.5.1
    ...     bp-moderation=0.1.4
    ...     buddypress-links=0.5
    ... packages-repo = http://downloads.wordpress.org/plugin
    ... destination = %(dest)s/plugins
    ...
    ... [mwextensions]
    ... recipe = leocornus.recipe.wpmw:deploy
    ... action = copy
    ... packages = 
    ...     Cite=r37577
    ...     SemanticForms=1.9.1
    ...     SemanticMediaWiki=1.5.1
    ... packages-repo = %(server)srepos
    ... destination = %(dest)s/extensions
    ... """ % dict(server=server, dest=dest))
    >>> print system(buildout)
    Uninstalling mwextensions.
    Uninstalling wpplugins.
    Installing wpplugins.
    wpplugins: Extracting package to .../sample-buildout/parts/wpplugins/buddypress-1.5.1
    wpplugins: Rename to .../dest/plugins/buddypress
    wpplugins: Extracting package to .../sample-buildout/parts/wpplugins/bp-moderation-0.1.4
    wpplugins: Rename to .../dest/plugins/bp-moderation
    wpplugins: Extracting package to .../sample-buildout/parts/wpplugins/buddypress-links-0.5
    wpplugins: Rename to .../dest/plugins/buddypress-links
    Installing mwextensions.
    mwextensions: Extracting package to .../sample-buildout/parts/mwextensions/Cite-r37577
    mwextensions: Rename to .../dest/extensions/Cite
    mwextensions: Extracting package to .../sample-buildout/parts/mwextensions/SemanticForms-1.9.1
    mwextensions: Rename to .../dest/extensions/SemanticForms
    mwextensions: Extracting package to .../sample-buildout/parts/mwextensions/SemanticMediaWiki-1.5.1
    mwextensions: Rename to .../dest/extensions/SemanticMediaWiki
    ...
    >>> ls(dest, 'plugins')
    d  bp-moderation
    d  buddypress
    d  buddypress-links
    >>> ls(dest, 'extensions')
    d  Cite
    d  SemanticForms
    d  SemanticMediaWiki

Examples for symlink recipe
===========================

preparing the packages.

    >>> target = tmpdir('target')
    >>> mkdir(target, 'dirone')
    >>> mkdir(target, 'dirtwo')
    >>> write(target, 'one.file', 
    ... """
    ... empty file for testing
    ... """)
    >>> ls(target)
    d  dirone
    d  dirtwo
    -  one.file
    >>> links = tmpdir('links')
    >>> ls(links)

get ready the buildout config for symlink.

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts = symlinks
    ...
    ... [symlinks]
    ... recipe = leocornus.recipe.wpmw:symlinks
    ... target-folder = %(target)s
    ... link-folder = %(link)s
    ... names = 
    ...     dirone
    ...     dirtwo
    ...     one.file
    ...     noexit.file
    ... """ % dict(target=target, link=links))

Run the buildout

    >>> print system(buildout)
    Uninstalling mwextensions.
    Uninstalling wpplugins.
    Installing symlinks.
    symlinks: Create symlink to .../links/dirone
    symlinks: Create symlink to .../links/dirtwo
    symlinks: Create symlink to .../links/one.file
    symlinks: Target .../target/noexit.file not exist, ignoring...

Verify the link folder.

    >>> ls(links)
    d  dirone
    d  dirtwo
    l  one.file
