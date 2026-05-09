from __future__ import annotations

import json
import logging
import re
from collections.abc import Callable
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.utils import timezone

from .models import Message, Tap

logger = logging.getLogger(__name__)


def is_json_serializable(obj: Any) -> bool:
    try:
        json.dumps(obj)
        return True
    except (TypeError, OverflowError):
        return False


class WiretapMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        request.wiretap_message = None  # type: ignore[attr-defined]
        if self._should_tap(request):
            self._log_request(request)

        response = self.get_response(request)

        if request.wiretap_message:  # type: ignore[attr-defined]
            self._log_response(request, response)

        return response

    def _should_tap(self, request: HttpRequest) -> bool:
        try:
            for tap in Tap.objects.filter(is_active=True):
                if re.search(tap.path, request.path):
                    return True
        except Exception:
            logger.exception(
                "Error occurred while fetching taps. No messages will be tapped."
            )
        return False

    def _log_request(self, request: HttpRequest) -> None:
        try:
            request.wiretap_message = Message()  # type: ignore[attr-defined]
            request.wiretap_message.started_at = timezone.now()  # type: ignore[attr-defined]
            request.wiretap_message.remote_addr = request.META.get("REMOTE_ADDR", None)  # type: ignore[attr-defined]
            request.wiretap_message.request_method = request.method  # type: ignore[attr-defined]
            request.wiretap_message.request_path = request.path  # type: ignore[attr-defined]
            headers: dict[str, str] = {}
            for key, value in request.headers.items():
                if is_json_serializable(key) and is_json_serializable(value):
                    if key.startswith("HTTP_"):
                        headers[key[5:]] = value
                    headers[key] = value
            request.wiretap_message.request_headers_json = json.dumps(headers, indent=2)  # type: ignore[attr-defined]
            request.wiretap_message.request_body_raw = request.body.decode("utf-8")  # type: ignore[attr-defined]
            if request.body:
                content_type = request.META.get("CONTENT_TYPE", "")
                request.wiretap_message.request_body_pretty = self._prettify(  # type: ignore[attr-defined]
                    content_type, request.body.decode("utf-8")
                )
        except Exception:
            logger.exception("Error occurred while logging request.")
        finally:
            request.wiretap_message.save()  # type: ignore[attr-defined]

    def _log_response(self, request: HttpRequest, response: HttpResponse) -> None:
        try:
            request.wiretap_message.ended_at = timezone.now()  # type: ignore[attr-defined]
            request.wiretap_message.duration = (  # type: ignore[attr-defined]
                request.wiretap_message.ended_at - request.wiretap_message.started_at  # type: ignore[attr-defined]
            ).total_seconds()
            request.wiretap_message.response_status_code = response.status_code  # type: ignore[attr-defined]
            request.wiretap_message.response_reason_phrase = response.reason_phrase  # type: ignore[attr-defined]
            headers = {}
            for key, value in response.items():
                if is_json_serializable(key) and is_json_serializable(value):
                    headers[key] = value
            request.wiretap_message.response_headers_json = json.dumps(  # type: ignore[attr-defined]
                headers, indent=2
            )
            request.wiretap_message.response_body_raw = response.content.decode("utf-8")  # type: ignore[attr-defined]
            if response.content:
                content_type = response.get("Content-Type", "")
                request.wiretap_message.response_body_pretty = self._prettify(  # type: ignore[attr-defined]
                    content_type, response.content.decode("utf-8")
                )
        except Exception:
            logger.exception("Error occurred while logging response.")
        finally:
            request.wiretap_message.save()  # type: ignore[attr-defined]

    def _prettify(self, content_type: str, content: str) -> str | None:
        result = None
        if content_type:
            try:
                if "json" in content_type:
                    result = json.loads(content)
                    result = json.dumps(result, indent=2)
            except Exception:
                pass
        return result
