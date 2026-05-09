import json
from unittest.mock import Mock, patch

import pytest
from django.test import RequestFactory

from wiretap.middleware import WiretapMiddleware
from wiretap.models import Message, Tap


@pytest.fixture()
def rf():
    return RequestFactory()


@pytest.fixture()
def middleware():
    mock_response = Mock()
    return WiretapMiddleware(mock_response)


def test_initialization(middleware):
    assert callable(middleware.get_response)


@pytest.mark.django_db
def test_no_taps(middleware, rf):
    assert Tap.objects.count() == 0
    middleware(rf.get("/"))
    assert Message.objects.count() == 0


@pytest.mark.django_db
def test_tap_match(rf):
    Tap.objects.create(path="/test", is_active=True)
    mock_response = Mock(
        items=dict().items,
        status_code=200,
        reason_phrase="OK",
        content=b"",
    )
    middleware = WiretapMiddleware(Mock(return_value=mock_response))
    middleware(rf.get("/test"))
    assert Message.objects.count() == 1


@pytest.mark.django_db
def test_tap_mismatch(middleware, rf):
    Tap.objects.create(path="/test", is_active=True)
    middleware(rf.get("/real"))
    assert Message.objects.count() == 0


@pytest.mark.django_db
def test_tap_not_active(middleware, rf):
    Tap.objects.create(path="/test", is_active=False)
    middleware(rf.get("/test"))
    assert Message.objects.count() == 0


@pytest.mark.django_db
def test_captures_json_request_and_response_bodies(rf):
    Tap.objects.create(path="/api", is_active=True)
    response = Mock(
        items=lambda: [("Content-Type", "application/json")],
        status_code=200,
        reason_phrase="OK",
        content=b'{"ok": true}',
    )
    response.get = lambda name, default="": (
        "application/json" if name == "Content-Type" else default
    )
    middleware = WiretapMiddleware(Mock(return_value=response))

    request = rf.post(
        "/api/echo",
        data=json.dumps({"hello": "world"}),
        content_type="application/json",
    )
    middleware(request)

    message = Message.objects.get()
    assert message.request_body_raw == '{"hello": "world"}'
    assert message.request_body_pretty is not None
    assert json.loads(message.request_body_pretty) == {"hello": "world"}
    assert message.response_body_raw == '{"ok": true}'
    assert message.response_body_pretty is not None
    assert json.loads(message.response_body_pretty) == {"ok": True}
    assert "Content-Type" in message.response_headers


@pytest.mark.django_db
def test_tap_query_exception_is_swallowed(middleware, rf, caplog):
    with patch.object(Tap.objects, "filter", side_effect=RuntimeError("db down")):
        response = middleware(rf.get("/anything"))
    assert response is middleware.get_response.return_value
    assert Message.objects.count() == 0
    assert "Error occurred while fetching taps" in caplog.text


@pytest.mark.django_db
def test_request_logging_exception_is_swallowed(rf, caplog):
    Tap.objects.create(path="/test", is_active=True)
    response = Mock(
        items=dict().items, status_code=200, reason_phrase="OK", content=b""
    )
    middleware = WiretapMiddleware(Mock(return_value=response))

    request = rf.post(
        "/test", data=b"\xff\xfe", content_type="application/octet-stream"
    )
    middleware(request)

    assert "Error occurred while logging request" in caplog.text
    assert Message.objects.count() == 1


@pytest.mark.django_db
def test_response_logging_exception_is_swallowed(rf, caplog):
    Tap.objects.create(path="/test", is_active=True)
    response = Mock(spec=[])  # accessing any attribute on response raises
    middleware = WiretapMiddleware(Mock(return_value=response))

    middleware(rf.get("/test"))

    assert "Error occurred while logging response" in caplog.text
    assert Message.objects.count() == 1
