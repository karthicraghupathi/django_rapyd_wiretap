import json

from django.db import models


class _NotSet(object):
    pass


class Tap(models.Model):
    path = models.CharField(
        max_length=255, help_text="The URL path to tap. Python regex is supported."
    )
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.path


class Message(models.Model):
    started_at = models.DateTimeField(db_index=True)
    ended_at = models.DateTimeField(null=True, blank=True, db_index=True)
    duration = models.PositiveIntegerField(null=True, blank=True, db_index=True)

    remote_addr = models.CharField(max_length=255, db_index=True)

    request_method = models.CharField(max_length=16, db_index=True)
    request_path = models.TextField(null=True, blank=True)
    request_headers_json = models.TextField()
    request_body_raw = models.TextField(null=True, blank=True)
    request_body_pretty = models.TextField(null=True, blank=True)

    response_status_code = models.PositiveIntegerField(
        blank=True, null=True, db_index=True
    )
    response_reason_phrase = models.CharField(
        max_length=64, blank=True, null=True, db_index=True
    )
    response_headers_json = models.TextField(blank=True, null=True)
    response_body_raw = models.TextField(null=True, blank=True)
    response_body_pretty = models.TextField(null=True, blank=True)

    @property
    def request_headers(self):
        return json.loads(self.request_headers_json)

    @property
    def response_headers(self):
        return json.loads(self.response_headers_json)

    def get_request_header(self, key, default=_NotSet):
        return self._get_header(self.request_headers, key, default)

    def get_response_header(self, key, default=_NotSet):
        return self._get_header(self.response_headers, key, default)

    def _get_header(self, headers, search_key, default):
        search_key = search_key.title()
        try:
            return next(value for (key, value) in headers if key == search_key)
        except StopIteration:
            if default is _NotSet:
                raise KeyError(search_key)
            else:
                return default

    def __str__(self):
        return "{} {}".format(self.request_method, self.request_path)
