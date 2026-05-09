import json
from unittest.mock import Mock

import pytest

from wiretap.middleware import WiretapMiddleware


@pytest.fixture()
def prettify():
    mw = WiretapMiddleware(Mock())
    return mw._prettify


def test_valid_json(prettify):
    result = prettify("application/json", '{"key": "value"}')
    assert json.loads(result) == {"key": "value"}


def test_invalid_json_returns_none(prettify):
    assert prettify("application/json", "not json") is None


def test_empty_body_returns_none(prettify):
    assert prettify("application/json", "") is None


def test_non_json_content_type_returns_none(prettify):
    assert prettify("text/html", "<html></html>") is None


def test_missing_content_type_returns_none(prettify):
    assert prettify("", '{"key": "value"}') is None


def test_json_is_pretty_printed(prettify):
    result = prettify("application/json", '{"b":2,"a":1}')
    assert result is not None
    assert "\n" in result
