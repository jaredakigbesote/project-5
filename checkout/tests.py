from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import patch, Mock
from decimal import Decimal
from workshops.models import WorkshopCategory, Instructor, Workshop, Session
from bookings.models import Booking
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class CheckoutFlowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="alice", email="a@a.com", password="pass12345")
        self.client.login(username="alice", password="pass12345")

        cat = WorkshopCategory.objects.create(name="Tech")
        instr = Instructor.objects.create(user=User.objects.create_user("inst", "i@i.com", "pass12345"))
        self.workshop = Workshop.objects.create(
            category=cat,
            title="Game Dev 101",
            instructor=instr,
            short_description="Intro",
            description="Full desc",
            base_price=Decimal("49.00"),
            is_active=True,
        )
        self.session = Session.objects.create(
            workshop=self.workshop,
            starts_at=timezone.now() + timedelta(days=1),
            ends_at=timezone.now() + timedelta(days=1, hours=2),
            capacity=10,
            seats_sold=0,
            location="Room 1",
        )

    @patch("checkout.views.stripe.PaymentIntent.create")
    def test_start_checkout_creates_booking_and_returns_pay_template(self, mock_create):
        mock_pi = Mock(id="pi_test_123", client_secret="pi_test_123_secret_abc")
        mock_create.return_value = mock_pi

        url = reverse("checkout:start", args=[self.session.id])
        resp = self.client.post(url, {"quantity": "2"})
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "checkout/pay.html")
        self.assertTrue(Booking.objects.filter(user=self.user, session=self.session, quantity=2).exists())

    def test_start_checkout_rejects_invalid_quantity(self):
        url = reverse("checkout:start", args=[self.session.id])
        resp = self.client.post(url, {"quantity": "0"})
        self.assertEqual(resp.status_code, 400)

    def test_start_checkout_rejects_over_capacity(self):
        url = reverse("checkout:start", args=[self.session.id])
        resp = self.client.post(url, {"quantity": "999"})
        self.assertEqual(resp.status_code, 400)

    @patch("checkout.views.stripe.PaymentIntent.retrieve")
    def test_success_marks_paid_and_decrements_seats_once(self, mock_retrieve):
        # Create pending booking
        b = Booking.objects.create(
            user=self.user, session=self.session, quantity=3,
            unit_price=self.workshop.base_price, total=Decimal("147.00"),
            stripe_pi="pi_test_123", paid=False
        )
        mock_pi = Mock(status="succeeded")
        mock_retrieve.return_value = mock_pi

        url = reverse("checkout:success", args=[b.id])
        # First hit decrements seats and marks paid
        resp1 = self.client.get(url)
        self.assertEqual(resp1.status_code, 200)
        self.session.refresh_from_db()
        b.refresh_from_db()
        self.assertTrue(b.paid)
        self.assertEqual(self.session.seats_sold, 3)

        # Second hit should not double-decrement
        resp2 = self.client.get(url)
        self.session.refresh_from_db()
        self.assertEqual(self.session.seats_sold, 3)
