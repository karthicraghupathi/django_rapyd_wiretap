# Django Rapyd Wiretap

[![Tests](https://github.com/karthicraghupathi/django_rapyd_wiretap/actions/workflows/test.yml/badge.svg)](https://github.com/karthicraghupathi/django_rapyd_wiretap/actions/workflows/test.yml)
[![PyPI version](https://img.shields.io/pypi/v/django-rapyd-wiretap)](https://pypi.org/project/django-rapyd-wiretap/)
[![Python versions](https://img.shields.io/pypi/pyversions/django-rapyd-wiretap)](https://pypi.org/project/django-rapyd-wiretap/)
[![Django versions](https://img.shields.io/pypi/djversions/django-rapyd-wiretap)](https://pypi.org/project/django-rapyd-wiretap/)
[![License](https://img.shields.io/pypi/l/django-rapyd-wiretap)](https://github.com/karthicraghupathi/django_rapyd_wiretap/blob/main/LICENSE)

A Django middleware that logs HTTP requests and responses to your database for auditing or troubleshooting purposes. Unlike similar packages, it works in **production** — logging is not gated on `settings.DEBUG`.

Inspired by [nathforge/django-wiretap](https://github.com/nathforge/django-wiretap).

## Install

```bash
pip install django-rapyd-wiretap
```

## Quickstart

1. Add `wiretap` to `INSTALLED_APPS`:

   ```python
   INSTALLED_APPS = [
       ...
       "wiretap",
   ]
   ```

2. Add the middleware to `MIDDLEWARE`:

   ```python
   MIDDLEWARE = [
       ...
       "wiretap.middleware.WiretapMiddleware",
   ]
   ```

3. Apply migrations:

   ```bash
   python manage.py migrate
   ```

## Usage

In the Django admin, create a **Tap** to configure which requests to capture:

- **Path** — a Python regex matched against the full request path with `re.search`.
- **Is active** — deactivate a tap without deleting it.

Each matched request is stored as a **Message** with the request method, path, headers, body, response status, and timing information. Messages are read-only in the admin.

### Tap recipes

| Goal | Path regex |
|---|---|
| Capture all `/api/` traffic | `^/api/` |
| Capture a specific endpoint exactly | `^/api/v1/payments/$` |
| Capture a versioned endpoint (any version) | `^/api/v\d+/payments/` |
| Capture everything | `/` |
| Capture everything **except** `/admin/` and `/static/` | `^/(?!admin/\|static/)` |
| Capture POSTs to webhooks (combine with another middleware filtering by method) | `^/webhooks/` |

The path regex is matched with `re.search`, not `re.fullmatch` — anchor with `^` if you want a prefix match, and add `$` if you want an exact match. Query strings are not part of the path; they're available on `Message.request_path` only if Django's path router includes them (it normally doesn't).

### Reading captured messages

Each `Message` row has the following fields:

| Field | Description |
|---|---|
| `started_at` / `ended_at` | When request logging began and response logging finished (UTC, indexed). |
| `duration` | Whole seconds between `started_at` and `ended_at` (indexed). For sub-second precision, compute from the timestamps directly. |
| `remote_addr` | Client IP from `REMOTE_ADDR` (indexed). If you sit behind a proxy, install `django.middleware.common.CommonMiddleware`-style IP unwrapping **before** `WiretapMiddleware`. |
| `request_method` | `GET`, `POST`, etc. (indexed). |
| `request_path` | Full request path (no query string). |
| `request_headers_json` / `response_headers_json` | JSON-encoded header dicts. Use the `request_headers` / `response_headers` properties to get a `dict`. |
| `request_body_raw` / `response_body_raw` | UTF-8-decoded body. Set to empty string for empty bodies; non-UTF-8 bodies are skipped (the row is still saved). |
| `request_body_pretty` / `response_body_pretty` | JSON-pretty-printed body, populated only when the corresponding `Content-Type` contains `json` and the body parses. `NULL` otherwise. |
| `response_status_code` / `response_reason_phrase` | HTTP status (indexed). |

Helper methods on `Message`:

```python
message.get_request_header("Content-Type")          # raises KeyError if missing
message.get_request_header("X-Custom", default=None)  # returns default if missing
message.get_response_header("Location", "")
```

Header lookups are case-insensitive (titled-cased internally).

## Operations

### Pruning old messages

`Message` rows accumulate forever once a Tap is active. A 100 RPS endpoint matched by `^/api/` produces ~8.6M rows/day — plan storage accordingly and prune on a schedule.

```bash
# delete messages older than 30 days
python manage.py wiretap_prune --older-than-days 30

# preview without deleting
python manage.py wiretap_prune --older-than-days 30 --dry-run
```

Run as a daily cron / scheduled job. The command issues a single bulk `DELETE` filtered on `started_at`.

### Middleware ordering

Place `WiretapMiddleware` near the top of `MIDDLEWARE`, after security/common middleware but before any middleware that mutates request bodies or response content. The earlier it sits, the closer the captured payload is to the on-the-wire form.

If you sit behind a load balancer or reverse proxy, install IP-unwrapping middleware (e.g., `django.middleware.common.CommonMiddleware` plus `USE_X_FORWARDED_HOST`, or a dedicated package) **before** `WiretapMiddleware`, so `remote_addr` reflects the real client IP rather than the proxy's.

### Indexed fields and ad-hoc queries

`started_at`, `ended_at`, `duration`, `remote_addr`, `request_method`, `response_status_code`, and `response_reason_phrase` are indexed. Filtering/ordering by those scales. Filtering by `request_path` (a `TextField`) on a large table will table-scan; if you do this often, add a custom index in your project's migrations.

### Sensitive data

Wiretap captures **everything** in matched requests, including `Authorization` and `Cookie` headers, request/response bodies, and any tokens or PII passing through. Tap conservatively, and keep the `Message` table on storage with the same threat model as your secrets store.

Built-in opt-in redaction is on the roadmap — see [issue #10](https://github.com/karthicraghupathi/django_rapyd_wiretap/issues/10).

## Supported versions

| Package | Versions |
|---|---|
| Python | 3.10, 3.11, 3.12, 3.13 |
| Django | 4.2 LTS, 5.2 LTS |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, test commands, and the release process.

## License

Apache 2.0. See [LICENSE](LICENSE).
