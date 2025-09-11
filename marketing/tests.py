from django.test import TestCase, Client
from django.urls import reverse
from marketing.models import NewsletterSubscriber

class MarketingSubscribeTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_subscribe_valid_email_creates_record(self):
        resp = self.client.post(reverse("marketing:subscribe"), {"email": "test@example.com"})
        self.assertIn(resp.status_code, (200, 302))  # template or redirect
        self.assertTrue(NewsletterSubscriber.objects.filter(email="test@example.com").exists())

    def test_subscribe_invalid_email_shows_error(self):
        resp = self.client.post(reverse("marketing:subscribe"), {"email": "not-an-email"})
        self.assertIn(resp.status_code, (200, 302))
        # Optional: you can assert messages or that no record was created
        self.assertFalse(NewsletterSubscriber.objects.filter(email="not-an-email").exists())
