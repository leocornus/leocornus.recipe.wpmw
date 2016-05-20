This doctest will try to test the process to download MediaWiki
extensions and skins from website:
htts://extdist.mwflabs.org/dist.

Preparing testing
=================

Get ready the testing folders.::

  >>> dest = tmpdir('dest')
  >>> mkdir(dest, 'extensions')
  >>> mkdir(dest, 'skins')

List the destination folder to make sure all testing folders are 
created.::

  >>> ls(dest)
  d extensions
  d skins
  >>> ls(dest, 'extensions')
  >>> ls(dest, 'skins')

Create the **buildout.cfg** file.::

  >>> write(sample_buildout, 'buildout.cfg',
  ... """
  ... [buildout]
  ... parts = 
  ...     mwskins
  ...     mwextensions
  ... 
  ... [mwskins]
  ... recipe = leocornus.recipe.wpmw:deploy
  ... packages = 
  ...     Example=REL1_26-6937930
  ...     Vector=REL1_26-186325f
  ... file-extension = .tar.gz
  ... separator = -
  ... packages-repo = https://extdist.wmflabs.org/dist/skins
  ... destination = %(dest)s/skins
  ...
  ... [mwextensions]
  ... recipe = leocornus.recipe.wpmw:deploy
  ... packages = 
  ...     Cite=REL1_26-dc872e6
  ...     SemanticForms=REL1_26-c514c90
  ...     CirrusSearch=REL1_26-c80d8ec
  ...     MultimediaViewer=REL1_26-a312b66
  ... file-extension = .tar.gz
  ... separator = -
  ... packages-repo = https://extdist.wmflabs.org/dist/extensions
  ... destination = %(dest)s/extensions
  ... """ % dict(dest=dest))

Run the buildout
================

execute the buildout::

  >>> print system(buildout)
  Installing mwskins.
  Downloading ...
  ...
  Downloading ...
  ...
  Installing mwextensions.
  Downloading ...
  ...
  Downloading ...
  ...
  Downloading ...
  ...

Check result
============

List the destination folder to verify the results.::

  >>> ls(dest, 'skins')
  d  Example
  d  Vector
  >>> ls(dest, 'extensions')
  d  CirrusSearch
  d  Cite
  d  MultimediaViewer
  d  SemanticForms
