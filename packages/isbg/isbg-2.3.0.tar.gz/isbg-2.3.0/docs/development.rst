Development
===========

Development schema
------------------

We should work in a ``feature/*`` branch or ``bugfix/*`` branch and it
should be attached to an **issue**.

Versioning schema
-----------------

We tag the new releases as:

  ``v{major_release_number}.{minor_release_number}.{patch_release_number}``

The current version number of **isbg** is stored in ``isbg/isbg.py``

Releasing Schema
----------------
You should:

#. Update the __version__ var ``./isbg/isbg.py``.
#. Update ``./NEWS.rst``
#. Update ``./Changelog.rst``
#. Check if some changes should be updated in ``./README.rst``
#. If new files have been added or removed: Check ``./MANIFEST.in``.
#. If dependencies have been updated, added or removed check: ``./setup.py``,
   ``./requirements.txt`` and/or ``./requirements-build.txt``.
#. Commit it to `master`.
#. Tag the new version
