Change History
**************

1.3.1 (2016-02-22)
=================

- fix some errors in test cases.
- adding travis CI.
- update document format to rst (re-Structure).

1.3.0 (2012-04-05)
==================

- Using the ``deploy`` recipe to replace both ``plugins`` and 
  ``extensions`` recipes.  Both recipes pretty much do the same
  work.

1.2.0 (2012-03-23)
==================

- Adding the ``action`` option for both ``plugins`` and ``extensions``
  recipes.  It has ``symlink`` as the default value and ``copy`` to 
  do hardcopy instead.

1.1.1 (2012-03-09)
==================

- Make sure to create symlinks during buildout updating.

1.1.0 (2012-03-07)
==================

- Add the part directory to install result, so buildout will remove
  it during uninstalling.

- New symlinks recipe to create symlinks from target folder to link
  folder for all names.

1.0.1 (2012-03-06)
==================

- Using os.path.lexists instead of os.path.exists to make sure the
  broken symlinks got removed.

1.0.0 (2012-03-05)
==================

- Initial release
