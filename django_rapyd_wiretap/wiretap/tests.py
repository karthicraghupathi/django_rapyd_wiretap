from django.test import RequestFactory, TestCase

from .middleware import WiretapMiddleware
from .models import Message, Tap


class WiretapTestCase(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def test_enabled_if_debugging(self):
        WiretapMiddleware()

    def test_no_taps(self):
        self.assertEqual(Tap.objects.count(), 0)
        WiretapMiddleware().process_request(self.request_factory.get("/"))
        self.assertEqual(Message.objects.count(), 0)

    def test_tap_match(self):
        Tap.objects.create(path="/test", is_active=True)
        WiretapMiddleware().process_request(self.request_factory.get("/test"))
        self.assertEqual(Message.objects.count(), 1)

    def test_tap_mismatch(self):
        Tap.objects.create(path="/test", is_active=True)
        WiretapMiddleware().process_request(self.request_factory.get("/real"))
        self.assertEqual(Message.objects.count(), 0)

    def test_tap_match_not_active(self):
        Tap.objects.create(path="/test", is_active=False)
        WiretapMiddleware().process_request(self.request_factory.get("/test"))
        self.assertEqual(Message.objects.count(), 0)
