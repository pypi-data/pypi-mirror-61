Changelog
=========


1.1 (2020-02-11)
----------------

- Improve the ``sql_quote`` fix.
  For details and discussion, see `DocumentTemplate <https://github.com/zopefoundation/DocumentTemplate/issues/48>`_.
  If you are not using SQL in your website you do **NOT** need to upgrade.
  (You can if you want to.)
  Default Plone does not need it.
  Upgrading to this version is especially recommended when you use Postgres.
  Note that ``RelStorage`` is not affected.
  Specific changes:

  - In ``sql_quote`` no longer escape double quotes and backslashes by doubling them:
    on MySQL this was fine, but on Postgres valid double quotes and backslashes
    would actually end up twice in the database.

  - In ``sql_quote`` remove the special ``\x1a`` NUL character and the carriage return ``\r``.
    This change is good for both MySQL and Postgres.


1.0 (2020-01-21)
----------------

- Initial release
