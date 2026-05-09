# Contributing

## Dev setup

Requires Python 3.10+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/karthicraghupathi/django_rapyd_wiretap.git
cd django_rapyd_wiretap
uv sync --extra dev
```

Install pre-commit hooks (runs ruff + mypy on every commit):

```bash
uv run pre-commit install
```

## Running tests

```bash
uv run pytest                         # all tests
uv run pytest --cov=wiretap           # with coverage
uv run tox                            # full matrix (Python 3.10-3.13 x Django 4.2/5.2)
```

## Linting and type checking

```bash
uv run ruff check .
uv run ruff format .
uv run mypy wiretap/
```

## Updating dependencies

After editing `pyproject.toml`:

```bash
uv lock
uv export --extra dev --format requirements-txt --no-hashes -o requirements-dev.txt
```

## Release process

1. Ensure all tests pass on `main`.
2. Bump the version:

   ```bash
   uv run bump-my-version bump minor   # or patch / major
   ```

3. Push the tag to GitHub:

   ```bash
   git push --tags
   ```

4. GitHub Actions creates a Release automatically, which triggers the PyPI publish workflow.

> **First-time PyPI publish:** before pushing a tag, configure a [Trusted Publisher](https://docs.pypi.org/trusted-publishers/) in PyPI project settings pointing at the `publish.yml` workflow and the `release` environment.
