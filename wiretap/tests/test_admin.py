import pytest
from django.contrib import admin
from django.test import RequestFactory

from wiretap.models import Message, Tap


@pytest.fixture()
def rf():
    return RequestFactory()


@pytest.mark.django_db
def test_tap_registered_with_admin():
    assert admin.site.is_registered(Tap)


@pytest.mark.django_db
def test_message_registered_with_admin():
    assert admin.site.is_registered(Message)


@pytest.mark.django_db
def test_message_admin_is_read_only(rf):
    message_admin = admin.site._registry[Message]
    request = rf.get("/")
    assert message_admin.has_add_permission(request) is False
    assert message_admin.has_change_permission(request) is False
    assert message_admin.has_delete_permission(request) is False
