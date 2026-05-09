from __future__ import annotations

from argparse import ArgumentParser
from datetime import timedelta
from typing import Any

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from wiretap.models import Message


class Command(BaseCommand):
    help = "Delete wiretap Message rows older than --older-than-days days."

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "--older-than-days",
            type=int,
            required=True,
            help=(
                "Delete messages whose started_at is older than this many days "
                "ago. Must be non-negative."
            ),
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Print how many rows would be deleted, then exit without deleting.",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        days: int = options["older_than_days"]
        if days < 0:
            raise CommandError("--older-than-days must be non-negative.")

        cutoff = timezone.now() - timedelta(days=days)
        qs = Message.objects.filter(started_at__lt=cutoff)
        count = qs.count()

        suffix = f"with started_at < {cutoff.isoformat()} ({days} day(s) ago)."

        if options["dry_run"]:
            self.stdout.write(f"Would delete {count} message(s) {suffix}")
            return

        deleted, _ = qs.delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {deleted} message(s) {suffix}"))
