from django.test import TestCase
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from workshops.models import WorkshopCategory, Instructor, Workshop, Session

User = get_user_model()

class WorkshopModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("inst", "i@i.com", "pass12345")
        self.cat = WorkshopCategory.objects.create(name="Design")
        self.instr = Instructor.objects.create(user=self.user)

    def test_slug_autogenerates(self):
        w = Workshop.objects.create(
            category=self.cat, title="UX Basics", instructor=self.instr,
            short_description="short", description="long",
            base_price=Decimal("10.00"), is_active=True
        )
        self.assertTrue(w.slug)
        self.assertIn("ux-basics", w.slug)

    def test_seats_remaining_property(self):
        w = Workshop.objects.create(
            category=self.cat, title="UI", instructor=self.instr,
            short_description="short", description="long",
            base_price=Decimal("10.00"), is_active=True
        )
        s = Session.objects.create(
            workshop=w,
            starts_at=timezone.now() + timedelta(days=1),
            ends_at=timezone.now() + timedelta(days=1, hours=2),
            capacity=8, seats_sold=3, location="Lab"
        )
        self.assertEqual(s.seats_remaining, 5)

