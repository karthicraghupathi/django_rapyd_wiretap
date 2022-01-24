import json
import logging
import re

from django.utils import timezone

from .models import Message, Tap

logger = logging.getLogger(__name__)


def is_json_serializable(obj):
    """
    Checks if an object is JSON serializable.
    """
    try:
        json.dumps(obj)
        return True
    except (TypeError, OverflowError):
        return False


class WiretapMiddleware:
    """
    Logs requests and responses to the DB.
    """

    def __init__(self, get_response):
        """
        Initialize the middleware.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Process requests and responses.

        If tracking is enabled for this request, perform the necessary logging.
        """
        # attempt log the request if the tap is enabled
        request.wiretap_message = None
        if self._should_tap(request):
            self._log_request(request)

        # let the request through for usual process
        response = self.get_response(request)

        # if we logged the request, then let's attempt to log the response
        if request.wiretap_message:
            self._log_response(request, response)

        # return the response
        return response

    def _should_tap(self, request):
        """
        Returns true if we should store the request/response.
        """
        try:
            for tap in Tap.objects.filter(is_active=True):
                if re.search(tap.path, request.path):
                    return True
        except Exception:
            logger.exception(
                "Error occurred while fetching taps. No messages will be tapped."
            )
        return False

    def _log_request(self, request):
        """
        Logs the request.
        """
        try:
            request.wiretap_message = Message()
            request.wiretap_message.started_at = timezone.now()
            request.wiretap_message.remote_addr = request.META.get("REMOTE_ADDR", None)
            request.wiretap_message.request_method = request.method
            request.wiretap_message.request_path = request.path
            headers = dict()
            for (key, value) in request.headers.items():
                if is_json_serializable(key) and is_json_serializable(value):
                    if key.startswith("HTTP_"):
                        headers[key[5:]] = value
                    headers[key] = value
            request.wiretap_message.request_headers_json = json.dumps(headers, indent=2)
            request.wiretap_message.request_body_raw = request.body.decode("utf-8")
            if request.body:
                content_type = request.META.get("CONTENT_TYPE", "")
                request.wiretap_message.request_body_pretty = self._prettify(
                    content_type, request.body.decode("utf-8")
                )
        except Exception:
            logger.exception("Error occurred while logging request.")
        finally:
            request.wiretap_message.save()

    def _log_response(self, request, response):
        """
        Logs the response.
        """
        try:
            request.wiretap_message.ended_at = timezone.now()
            request.wiretap_message.duration = (
                request.wiretap_message.ended_at - request.wiretap_message.started_at
            ).total_seconds()
            request.wiretap_message.response_status_code = response.status_code
            request.wiretap_message.response_reason_phrase = response.reason_phrase
            headers = dict()
            for (key, value) in response.items():
                if is_json_serializable(key) and is_json_serializable(value):
                    headers[key] = value
            request.wiretap_message.response_headers_json = json.dumps(
                headers, indent=2
            )
            request.wiretap_message.response_body_raw = response.content.decode("utf-8")
            if response.content:
                content_type = response.get("Content-Type", "")
                request.wiretap_message.response_body_pretty = self._prettify(
                    content_type, response.content.decode("utf-8")
                )
        except Exception:
            logger.exception("Error occurred while logging response.")
        finally:
            request.wiretap_message.save()

    def _prettify(self, content_type, content):
        """
        Tries to prettify the content. If not, returns None.
        """
        result = None
        if content_type:
            try:
                if "json" in content_type:
                    result = json.loads(content)
                    result = json.dumps(result, indent=2)
            except Exception:
                pass  # do nothing
        return result
