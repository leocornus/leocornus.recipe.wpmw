
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

``action``

    There are 2 values for this option: ``symlink`` and ``copy``.
    Default value is ``symlink``.  This option will be ignored for ``symlink``
    recipe.  

Options for plugins recipe:

``plugins``

    A list of plugins id and version at format id=version. 
    e.g. buddypress=1.5.1

``plugins-repo``

    The base URL to download the plugins, default is
    ``http://downloads.wordpress.org/plugin``.  This option allow user to get
    plugins from an interal repository.

``wordpress-root``

    The root folder of WordPress installation.  The wp-content/plugins folder
    is within it.

Options for extensions recipe:

``extensions``

    A list of extensions id and version at format id=version.
    e.g. SemanticForms=2.4

``extensions-repo``

    The base URL, where we could download the extensions.

``mediawiki-root``

    The root folder of MediaWiki installation.  We will create symlink in its
    extensions sub-folder.

Options for symlink recipe:

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

Examples for WordPress Plugins
==============================

get ready a empty WordPress plugins folder for testing.

    >>> import os.path
    >>> wordpress = tmpdir('wordpress')
    >>> mkdir(wordpress, 'wp-content')
    >>> ls(wordpress)
    d  wp-content
    >>> mkdir(wordpress, 'wp-content', 'plugins')
    >>> ls(wordpress, 'wp-content')
    d  plugins

try to crate a symlink in plugins folder to test the unlink function.

    >>> import os
    >>> bp = tmpdir('bp-fake')
    >>> print bp
    /tmp/.../bp-fake
    >>> os.symlink(bp, os.path.join(wordpress, 'wp-content', 'plugins', 'buddypress'))
    >>> ls(wordpress, 'wp-content', 'plugins')
    d  buddypress

create a broken symlink, we have to use ``os.path.lexists`` to check the link name exist or
not.

    >>> bplink = tmpdir('bp-link')
    >>> os.symlink(bplink, os.path.join(wordpress, 'wp-content', 'plugins', 'buddypress-links'))
    >>> ls(wordpress, 'wp-content', 'plugins')
    d  buddypress
    d  buddypress-links
    >>> remove(bplink)
    >>> ls(wordpress, 'wp-content', 'plugins')
    d  buddypress
    l  buddypress-links

Try to run the Plugins recipe.  The ``sample_buildout`` is a built-in buildout object 
provided by zc.buildout.testing package.

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts = wpplugins
    ...
    ... [wpplugins]
    ... recipe = leocornus.recipe.wpmw:plugins
    ... plugins = 
    ...     buddypress=1.5.1
    ...     bp-moderation=0.1.4
    ...     buddypress-links=0.5
    ... wordpress-root = %(wordpress)s
    ... """ % dict(wordpress=wordpress))

Run the buildout

    >>> print system(buildout)
    Installing wpplugins.
    Downloading http://downloads.wordpress.org/plugin/buddypress.1.5.1.zip
    wpplugins: Extracting package to .../sample-buildout/parts/wpplugins/buddypress-1.5.1
    wpplugins: Create symlink to .../wordpress/wp-content/plugins/buddypress
    Downloading http://downloads.wordpress.org/plugin/bp-moderation.0.1.4.zip
    wpplugins: Extracting package to .../sample-buildout/parts/wpplugins/bp-moderation-0.1.4
    wpplugins: Create symlink to .../wordpress/wp-content/plugins/bp-moderation
    Downloading http://downloads.wordpress.org/plugin/buddypress-links.0.5.zip
    wpplugins: Extracting package to .../sample-buildout/parts/wpplugins/buddypress-links-0.5
    wpplugins: Create symlink to .../wordpress/wp-content/plugins/buddypress-links

Check the parts folder to make sure all plugins are downloaded.

    >>> ls(sample_buildout, 'parts')
    d  buildout
    d  wpplugins

    >>> ls(sample_buildout, 'parts', 'wpplugins')
    d  bp-moderation-0.1.4
    d  buddypress-1.5.1
    d  buddypress-links-0.5

check the WordPress plugins folder to make sure all symlink are created.

    >>> ls(wordpress, 'wp-content', 'plugins')
    d  bp-moderation
    d  buddypress
    d  buddypress-links

testing the copy action.  We should not expect download now, since the 
buildout will get them from download cache.

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts = wpplugins
    ...
    ... [wpplugins]
    ... recipe = leocornus.recipe.wpmw:plugins
    ... action = copy
    ... plugins = 
    ...     buddypress=1.5.1
    ...     bp-moderation=0.1.4
    ...     buddypress-links=0.5
    ... wordpress-root = %(wordpress)s
    ... """ % dict(wordpress=wordpress))
    >>> print system(buildout)
    Uninstalling wpplugins.
    Installing wpplugins.
    wpplugins: Extracting package to .../sample-buildout/parts/wpplugins/buddypress-1.5.1
    wpplugins: Rename to .../wordpress/wp-content/plugins/buddypress
    wpplugins: Extracting package to .../sample-buildout/parts/wpplugins/bp-moderation-0.1.4
    wpplugins: Rename to .../wordpress/wp-content/plugins/bp-moderation
    wpplugins: Extracting package to .../sample-buildout/parts/wpplugins/buddypress-links-0.5
    wpplugins: Rename to .../wordpress/wp-content/plugins/buddypress-links
    >>> ls(wordpress, 'wp-content', 'plugins')
    d  bp-moderation
    d  buddypress
    d  buddypress-links

Examples for MediaWiki Extensions
=================================

We need a temp server for this testing

    >>> import os.path
    >>> testdata = join(os.path.dirname(__file__), 'testdata')
    >>> server = start_server(testdata)

Prepare an empty MediaWiki extensions folder for testing

    >>> mediawiki = tmpdir('mediawiki')
    >>> mkdir(mediawiki, 'extensions')
    >>> ls(mediawiki)
    d  extensions

A simple buildout configuration file.

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts = mwextensions
    ... 
    ... [mwextensions]
    ... recipe = leocornus.recipe.wpmw:extensions
    ... extensions = 
    ...     Cite=r37577
    ...     SemanticForms=1.9.1
    ...     SemanticMediaWiki=1.5.1
    ... extensions-repo = %(server)srepos
    ... mediawiki-root = %(mediawiki)s
    ... """ % dict(server=server, mediawiki=mediawiki))

Run the buildout and check the result.

    >>> print system(buildout)
    Uninstalling wpplugins.
    Installing mwextensions.
    Downloading http://.../repos/Cite.r37577.zip
    mwextensions: Extracting package to .../sample-buildout/parts/mwextensions/Cite-r37577
    mwextensions: Create symlink to .../mediawiki/extensions/Cite
    Downloading http://.../repos/SemanticForms.1.9.1.zip
    mwextensions: Extracting package to .../sample-buildout/parts/mwextensions/SemanticForms-1.9.1
    mwextensions: Create symlink to .../mediawiki/extensions/SemanticForms
    Downloading http://.../repos/SemanticMediaWiki.1.5.1.zip
    mwextensions: Extracting package to .../sample-buildout/parts/mwextensions/SemanticMediaWiki-1.5.1
    mwextensions: Create symlink to .../mediawiki/extensions/SemanticMediaWiki

check the parts folder.

    >>> ls(sample_buildout, 'parts')
    d  buildout
    d  mwextensions
    >>> ls(sample_buildout, 'parts', 'mwextensions')
    d  Cite-r37577
    d  SemanticForms-1.9.1
    d  SemanticMediaWiki-1.5.1

check the MediaWiki extensions folder

    >>> ls(mediawiki, 'extensions')
    d  Cite
    d  SemanticForms
    d  SemanticMediaWiki

Test the copy action.

    >>> write(sample_buildout, 'buildout.cfg',
    ... """
    ... [buildout]
    ... parts = mwextensions
    ... 
    ... [mwextensions]
    ... recipe = leocornus.recipe.wpmw:extensions
    ... action = copy
    ... extensions = 
    ...     Cite=r37577
    ...     SemanticForms=1.9.1
    ...     SemanticMediaWiki=1.5.1
    ... extensions-repo = %(server)srepos
    ... mediawiki-root = %(mediawiki)s
    ... """ % dict(server=server, mediawiki=mediawiki))
    >>> print system(buildout)
    Uninstalling mwextensions.
    Installing mwextensions.
    mwextensions: Extracting package to .../sample-buildout/parts/mwextensions/Cite-r37577
    mwextensions: Rename to .../mediawiki/extensions/Cite
    mwextensions: Extracting package to .../sample-buildout/parts/mwextensions/SemanticForms-1.9.1
    mwextensions: Rename to .../mediawiki/extensions/SemanticForms
    mwextensions: Extracting package to .../sample-buildout/parts/mwextensions/SemanticMediaWiki-1.5.1
    mwextensions: Rename to .../mediawiki/extensions/SemanticMediaWiki
    >>> ls(mediawiki, 'extensions')
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
