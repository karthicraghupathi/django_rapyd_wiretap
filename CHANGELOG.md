# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-05-09

### Added

- `wiretap_prune` management command for retention. Run
  `python manage.py wiretap_prune --older-than-days 30` (or `--dry-run` to preview)
  to bulk-delete old `Message` rows by `started_at`.
- README sections on Tap recipes, reading captured `Message` fields, middleware
  ordering, indexed fields, and sensitive-data caveats. Pointer to the redaction
  enhancement tracked in [issue #10](https://github.com/karthicraghupathi/django_rapyd_wiretap/issues/10).

### Changed

- `publish.yml` now triggers on `push.tags: ['v*']` instead of `release.published`,
  so the auto-publish workflow fires reliably from a tag push without depending on
  GitHub's `GITHUB_TOKEN`-anti-recursion-blocked release event chain.

### Fixed

- Removed an unreachable `HTTP_`-prefix-stripping branch in
  `WiretapMiddleware._log_request` left over from when the header loop iterated
  `request.META`. The check never fires today, since `request.headers.items()`
  exposes headers in their HTTP form.
- README rendering on the GitHub project page: the Install and Quickstart code
  blocks had backslash-escaped triple-backticks (leftover from the original
  heredoc-generated rewrite) that GitHub rendered as literal text, collapsing
  each fenced block onto a single line. Replaced with literal triple-backticks.
- Django versions badge: switched from a nonexistent shields.io endpoint
  (`pypi/frameworkversions/django/...`) to the documented `pypi/djversions/...`,
  so the badge now shows `4.2 | 5.2` instead of "Django versions are missing".

### Internal

- Whole-package test coverage at 100% (44 tests). Middleware coverage 85% → 100%
  with new tests for body capture (JSON request/response), the tap-query exception
  path, and the request- and response-logging exception paths.

## [0.1.0] - 2026-05-09

### Added

- Full PEP 621 packaging via hatchling; single-source version in `wiretap/__init__.py`.
- `py.typed` marker (PEP 561) for typed-package consumers.
- Type annotations across `middleware.py`, `models.py`, `admin.py`, `apps.py`.
- GitHub Actions workflows: test matrix (Python 3.10–3.13 × Django 4.2/5.2), lint, build
  smoke test, OIDC PyPI publish, and automated GitHub Releases.
- Dependabot config for pip, github-actions, and pre-commit ecosystems.
- Pytest test suite (34 tests): middleware, models, admin, `_prettify`, `is_json_serializable`.
- `CONTRIBUTING.md`, `SECURITY.md`, and this `CHANGELOG.md`.
- `bump-my-version` replaces the unmaintained `bump2version`.
- Ruff replaces flake8 / isort / black.

### Changed

- Minimum Python version raised to **3.10** (dropped 3.6–3.9).
- Minimum Django version raised to **4.2 LTS** (dropped 3.2 and earlier).
- `uv` is now the recommended package manager for development.

### Fixed

- `Message._get_header` was iterating over dict keys instead of items (latent bug).
- `Message.response_headers` property crashed when `response_headers_json` is `NULL`.

### Removed

- `setup.py`, `setup.cfg`, `Pipfile`, `requirements.txt` — replaced by `pyproject.toml` + `uv`.
- `testrunner.py` — replaced by `pytest`.

[Unreleased]: https://github.com/karthicraghupathi/django_rapyd_wiretap/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/karthicraghupathi/django_rapyd_wiretap/releases/tag/v0.2.0
[0.1.0]: https://github.com/karthicraghupathi/django_rapyd_wiretap/releases/tag/v0.1.0
