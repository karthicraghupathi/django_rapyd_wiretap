from datetime import timedelta
from io import StringIO

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from django.utils import timezone

from wiretap.models import Message


@pytest.fixture()
def make_message(db):
    def _make(started_at):
        return Message.objects.create(
            started_at=started_at,
            remote_addr="127.0.0.1",
            request_method="GET",
            request_path="/test",
            request_headers_json="{}",
        )

    return _make


@pytest.mark.django_db
def test_prune_deletes_messages_older_than_threshold(make_message):
    now = timezone.now()
    old = make_message(now - timedelta(days=40))
    recent = make_message(now - timedelta(days=5))

    out = StringIO()
    call_command("wiretap_prune", "--older-than-days", "30", stdout=out)

    assert not Message.objects.filter(pk=old.pk).exists()
    assert Message.objects.filter(pk=recent.pk).exists()
    assert "Deleted 1 message" in out.getvalue()


@pytest.mark.django_db
def test_prune_keeps_everything_when_nothing_old(make_message):
    msg = make_message(timezone.now() - timedelta(days=5))

    out = StringIO()
    call_command("wiretap_prune", "--older-than-days", "30", stdout=out)

    assert Message.objects.filter(pk=msg.pk).exists()
    assert "Deleted 0 message" in out.getvalue()


@pytest.mark.django_db
def test_prune_dry_run_reports_count_without_deleting(make_message):
    msg = make_message(timezone.now() - timedelta(days=40))

    out = StringIO()
    call_command("wiretap_prune", "--older-than-days", "30", "--dry-run", stdout=out)

    assert Message.objects.filter(pk=msg.pk).exists()
    assert "Would delete 1 message" in out.getvalue()


@pytest.mark.django_db
def test_prune_zero_days_deletes_everything(make_message):
    now = timezone.now()
    older = make_message(now - timedelta(seconds=10))

    out = StringIO()
    call_command("wiretap_prune", "--older-than-days", "0", stdout=out)

    assert not Message.objects.filter(pk=older.pk).exists()
    assert "Deleted 1 message" in out.getvalue()


@pytest.mark.django_db
def test_prune_negative_days_raises_command_error(make_message):
    msg = make_message(timezone.now())

    with pytest.raises(CommandError, match="must be non-negative"):
        call_command("wiretap_prune", "--older-than-days", "-1")

    assert Message.objects.filter(pk=msg.pk).exists()


@pytest.mark.django_db
def test_prune_requires_older_than_days_argument():
    with pytest.raises(CommandError, match="required"):
        call_command("wiretap_prune")
