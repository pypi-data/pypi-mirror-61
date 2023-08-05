Plone hotfix, 2020-01-21
========================

This hotfix fixes several security issues:

- Privilege escalation when ``plone.restapi`` is installed.
  Reported and fixed by Lukas Graf and Niklaus Johner.

- An open redirection on the login form and possibly other places where redirects are done.
  The ``isURLInPortal`` check that is done to avoid linking to an external site could be tricked into accepting malicious links.
  Reported by Damiano Esposito.

- Password strength checks were not always checked.
  Reported by Ben Kummer.

- You might be able to PUT (overwrite) some content without needing write permission.
  This seems hard to do in practice.
  This fix is only needed when you use ``plone.app.contenttypes``.
  Reported and fixed by Alessandro Pisa.

- SQL quoting in DTML or in connection objects was insufficient, leading to possible SQL injections.
  This is a problem in Zope.  If you use Zope without Plone, this hotfix should work for you too.
  Reported and fixed by Michael Brunnbauer and Michael Howitz.

- Cross Site Scripting (XSS) in the title field on plone 5.0 and higher.
  Reported by Marcos Valle.


Compatibility
=============

This hotfix should be applied to the following versions of Plone:

* Plone 5.2.1 and any earlier 5.2.x version
* Plone 5.1.6 and any earlier 5.x version
* Plone 4.3.19 and any earlier 4.x version

The hotfix is officially supported by the Plone security team on the
following versions of Plone in accordance with the Plone
`version support policy <https://plone.org/security/update-policy>`_: 4.3.19, 5.0.10, 5.1.6 and 5.2.1.

On Plone 4.3, 5.0 and 5.1 the hotfix is officially only supported on Python 2.7.
On Plone 5.2.X it is supported on Python 2.7 and Python 3.6/3.7.

Python 2.6 should work, and earlier Plone 4 versions should work too, but this has not been fully tested.

The fixes included here will be incorporated into subsequent releases of Plone,
so Plone 4.3.20, 5.1.7, 5.2.2 and greater should not require this hotfix.


Installation
============

Installation instructions can be found at
https://plone.org/security/hotfix/20200121

.. note::

  You may get an error when running buildout::

    Error: Couldn't find a distribution for 'Products.PloneHotfix20200121==1.0'.

  The most likely cause is that your buildout is trying to download the hotfix via http or from an older PyPI index.
  In the buildout section of your buildout, make sure you use the correct index::

    [buildout]
    index = https://pypi.org/simple/


Q&A
===

Q: How can I confirm that the hotfix is installed correctly and my site is protected?
  A: On startup, the hotfix will log a number of messages to the Zope event log
  that look like this::

      2020-01-21 13:10:26 INFO Products.PloneHotfix20200121 Applied sql_quote patch
      2020-01-21 13:10:26 INFO Products.PloneHotfix20200121 Applied in_portal patch
      2020-01-21 13:10:26 INFO Products.PloneHotfix20200121 Applied password_validation patch
      2020-01-21 13:10:26 INFO Products.PloneHotfix20200121 Applied pac patch
      2020-01-21 13:10:26 INFO Products.PloneHotfix20200121 Applied content patch
      2020-01-21 13:10:26 INFO Products.PloneHotfix20200121 Applied layout patch
      2020-01-21 13:10:26 INFO Products.PloneHotfix20200121 Applied restapi_local_roles patch
      2020-01-21 13:10:26 INFO Products.PloneHotfix20200121 Hotfix installed

  The exact number of patches applied, will differ depending on what packages you are using.
  If a patch is attempted but fails, it will be logged as an error that says
  "Could not apply". This may indicate that you have a non-standard Plone
  installation.  Please investigate, and mail us the accompanying traceback if you think it is a problem in the hotfix.

Q: How can I report problems installing the patch?
  A: Contact the Plone security team at security@plone.org or visit the
  Gitter channel at https://gitter.im/plone/public and the forum at https://community.plone.org

Q: How can I report other potential security vulnerabilities?
  A: Please email the security team at security@plone.org rather than discussing
  potential security issues publicly.
