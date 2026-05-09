# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/karthicraghupathi/django_rapyd_wiretap/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/karthicraghupathi/django_rapyd_wiretap/releases/tag/v0.1.0
