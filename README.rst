====================
Django Rapyd Wiretap
====================

Logs requests and responses to your application in a DB for auditing or troubleshooting purposes.

Inspiration
-----------

This is heavily inspired by and borrows a lot from `nathforge/django-wiretap <https://github.com/nathforge/django-wiretap>`_.

**Why a new package?**

The fundamental difference is not letting ``settings.DEBUG`` determine if a message should be tapped. I have needs, yes in *PRODUCTION*, where this is useful to me.

Usage
-----

- Install the package with:
  ::

    pip install django-rapyd-wiretap

- Edit Django settings:

  - Add ``wiretap`` to ``INSTALLED_APPS``.
  - Add ``wiretap.middleware.WiretapMiddleware`` to your ``MIDDLEWARE_CLASSES``.

- Create models with:
  ::

    ./manage.py migrate

- Go to Django admin, add a new ``Tap``.

  - This contains a ``path``, which is matched against the full path including the query string. A valid regex is allowed here.
  - For example, to capture everything within the ``/api/`` path of your site, use ``^/api/``.
  - To capture everything, set it to ``/``.

To Do
-----

- Add support for configuring retention per tap and deleting older messages.
- Add support for prettifying major content types for easy troubleshooting.
- Delegate logging request and response bodies to a separate file on the file system keeping the DB lean for faster queries. Maybe? I'm still divided on this.
- I'm sure there are other things I haven't thought of yet or those that will be needed by the community.
