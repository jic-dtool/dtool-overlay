CHANGELOG
=========

This project uses `semantic versioning <http://semver.org/>`_.
This change log uses principles from `keep a changelog <http://keepachangelog.com/>`_.

[Unreleased]
------------

Added
^^^^^


Changed
^^^^^^^

- Changed ordering of lines in overlay CSV template from being sorted by the
  identifier to being ordered by the relpath


Deprecated
^^^^^^^^^^


Removed
^^^^^^^


Fixed
^^^^^



Security
^^^^^^^^


[0.2.0] - 2019-09-06
--------------------

Changed
^^^^^^^

- Made invocation of 'dtool overlays template parse' easier by removing need for glob_rule

Fixed
^^^^^

- Improved the help text in the CLI commands


[0.1.0] - 2019-09-04
--------------------

Initial release.

Added
^^^^^

- The CLI command 'dtool overlays show'
- The CLI command 'dtool overlays write'
- The CLI command 'dtool overlays template glob'
- The CLI command 'dtool overlays template pairs'
- The CLI command 'dtool overlays template parse'
