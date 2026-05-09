import pytest
from django.contrib import admin

from wiretap.models import Message, Tap


@pytest.mark.django_db
def test_tap_registered_with_admin():
    assert admin.site.is_registered(Tap)


@pytest.mark.django_db
def test_message_registered_with_admin():
    assert admin.site.is_registered(Message)
