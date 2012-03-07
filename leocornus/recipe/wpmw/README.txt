
This recipe should have 2 major functions: WordPress Plugins and 
MediaWiki Extensions

Options
=======

The ``leocornus.recipe.wpmw:Plugins`` recipe could be used to download WordPress
Plugins package, extract to certain folder, and create the symlink to WordPress
wp-content/plugins folder.  It supports the following general options:

Options for all recipes:

``ignore-existing``

    default is true, ignore existing folder.

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

create a broken symlink, we have to use os.path.lexists to check the link name exist or
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
