import json

import pytest
from django.utils import timezone

from wiretap.models import Message, Tap


@pytest.fixture()
def message(db):
    return Message.objects.create(
        started_at=timezone.now(),
        remote_addr="127.0.0.1",
        request_method="GET",
        request_path="/api/test",
        request_headers_json=json.dumps({"Content-Type": "application/json"}),
        response_headers_json=json.dumps({"X-Frame-Options": "DENY"}),
    )


def test_tap_str(db):
    tap = Tap.objects.create(path="/api/.*", is_active=True)
    assert str(tap) == "/api/.*"


def test_message_str(message):
    assert str(message) == "GET /api/test"


def test_request_headers_property(message):
    assert message.request_headers == {"Content-Type": "application/json"}


def test_response_headers_property(message):
    assert message.response_headers == {"X-Frame-Options": "DENY"}


def test_response_headers_null(db):
    msg = Message.objects.create(
        started_at=timezone.now(),
        remote_addr="127.0.0.1",
        request_method="GET",
        request_path="/",
        request_headers_json="{}",
        response_headers_json=None,
    )
    assert msg.response_headers == {}


def test_get_request_header(message):
    assert message.get_request_header("Content-Type") == "application/json"


def test_get_request_header_case_insensitive(message):
    assert message.get_request_header("content-type") == "application/json"


def test_get_request_header_missing_raises(message):
    with pytest.raises(KeyError):
        message.get_request_header("Authorization")


def test_get_request_header_default(message):
    assert message.get_request_header("Authorization", default=None) is None


def test_get_response_header(message):
    assert message.get_response_header("X-Frame-Options") == "DENY"


def test_get_response_header_missing_raises(message):
    with pytest.raises(KeyError):
        message.get_response_header("Content-Type")
