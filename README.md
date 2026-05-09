# Django Rapyd Wiretap

[![Tests](https://github.com/karthicraghupathi/django_rapyd_wiretap/actions/workflows/test.yml/badge.svg)](https://github.com/karthicraghupathi/django_rapyd_wiretap/actions/workflows/test.yml)
[![PyPI version](https://img.shields.io/pypi/v/django-rapyd-wiretap)](https://pypi.org/project/django-rapyd-wiretap/)
[![Python versions](https://img.shields.io/pypi/pyversions/django-rapyd-wiretap)](https://pypi.org/project/django-rapyd-wiretap/)
[![Django versions](https://img.shields.io/pypi/frameworkversions/django/django-rapyd-wiretap)](https://pypi.org/project/django-rapyd-wiretap/)
[![License](https://img.shields.io/pypi/l/django-rapyd-wiretap)](https://github.com/karthicraghupathi/django_rapyd_wiretap/blob/main/LICENSE)

A Django middleware that logs HTTP requests and responses to your database for auditing or troubleshooting purposes. Unlike similar packages, it works in **production** — logging is not gated on `settings.DEBUG`.

Inspired by [nathforge/django-wiretap](https://github.com/nathforge/django-wiretap).

## Install

\`\`\`bash
pip install django-rapyd-wiretap
\`\`\`

## Quickstart

1. Add `wiretap` to `INSTALLED_APPS`:

   \`\`\`python
   INSTALLED_APPS = [
       ...
       "wiretap",
   ]
   \`\`\`

2. Add the middleware to `MIDDLEWARE`:

   \`\`\`python
   MIDDLEWARE = [
       ...
       "wiretap.middleware.WiretapMiddleware",
   ]
   \`\`\`

3. Apply migrations:

   \`\`\`bash
   python manage.py migrate
   \`\`\`

## Usage

In the Django admin, create a **Tap** to configure which requests to capture:

- **Path** — a Python regex matched against the full request path.
- **Is active** — deactivate a tap without deleting it.

### Examples

| Goal | Path regex |
|---|---|
| Capture all `/api/` traffic | `^/api/` |
| Capture everything | `/` |
| Capture a specific endpoint | `^/api/v1/payments/$` |

Each matched request is stored as a **Message** with the request method, path, headers, body, response status, and timing information. Messages are read-only in the admin.

## Supported versions

| Package | Versions |
|---|---|
| Python | 3.10, 3.11, 3.12, 3.13 |
| Django | 4.2 LTS, 5.2 LTS |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, test commands, and the release process.

## License

Apache 2.0. See [LICENSE](LICENSE).
