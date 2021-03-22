from unittest.mock import Mock

from django.test import RequestFactory, TestCase

from .middleware import WiretapMiddleware
from .models import Message, Tap


class WiretapTestCase(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        self.mock = Mock()
        self.wiretap_middleware = WiretapMiddleware(self.mock)

    def test_initialization(self):
        self.assertEqual(self.wiretap_middleware.get_response, self.mock)

    def test_no_taps(self):
        self.assertEqual(Tap.objects.count(), 0)
        self.wiretap_middleware(self.request_factory.get("/"))
        self.assertEqual(Message.objects.count(), 0)

    def test_tap_match(self):
        Tap.objects.create(path="/test", is_active=True)
        self.mock.side_effect = [
            Mock(
                name="response",
                items=dict().items,
                status_code=200,
                reason_phrase="OK",
                content=b"",
            )
        ]
        self.wiretap_middleware(self.request_factory.get("/test"))
        self.assertEqual(Message.objects.count(), 1)

    def test_tap_mismatch(self):
        Tap.objects.create(path="/test", is_active=True)
        self.wiretap_middleware(self.request_factory.get("/real"))
        self.assertEqual(Message.objects.count(), 0)

    def test_tap_not_active(self):
        Tap.objects.create(path="/test", is_active=False)
        self.wiretap_middleware(self.request_factory.get("/test"))
        self.assertEqual(Message.objects.count(), 0)
