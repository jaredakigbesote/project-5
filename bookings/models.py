from django.db import models
from django.conf import settings
from workshops.models import Session
from django.core.validators import MinValueValidator

class Booking(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="bookings")
    session=models.ForeignKey(Session,on_delete=models.PROTECT,related_name="bookings")
    quantity=models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price=models.DecimalField(max_digits=8, decimal_places=2)
    total=models.DecimalField(max_digits=9, decimal_places=2)
    stripe_pi=models.CharField(max_length=120, blank=True)
    paid=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.user} x{self.quantity} for {self.session}"
