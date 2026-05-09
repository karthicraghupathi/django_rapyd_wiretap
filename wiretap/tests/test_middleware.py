from unittest.mock import Mock

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
