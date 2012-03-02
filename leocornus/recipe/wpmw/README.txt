
This recipe should have 2 major functions: WordPress Plugins and 
MediaWiki Extensions

Options
=======

The ``leocornus.recipe.wpmw:Plugins`` recipe could be used to download WordPress
Plugins package, extract to certain folder, and create the symlink to WordPress
wp-content/plugins folder.  It supports the following options:

``plugins``

    A list of plugins id and version at format id=version. 
    e.g. buddypress=1.5.1

``plugins-repo``

    The base URL to download the plugins, default is
    ``http://downloads.wordpress.org/plugin``.  This option allow user to get plugins
    from an interal repository.

``wordpress-root``

    The root folder of WordPress installation.  The wp-content/plugins folder is 
    within it.

``ignore-existing``

    default is true, ignore existing folder.

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

Check the parts folder and bin folder.

    >>> ls(sample_buildout, 'parts')
    d  buildout
    d  plugins

    >>> ls(sample_buildout, 'parts', 'plugins')
    d  bp-moderation-0.1.4
    d  buddypress-1.5.1
    d  buddypress-links-0.5
