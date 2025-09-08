from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
import stripe
from bookings.models import Booking
from workshops.models import Session

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def start_checkout(request, session_id):
    sess = get_object_or_404(Session, pk=session_id, workshop__is_active=True)
    qty = int(request.POST.get("quantity", 1))
    if qty < 1: return HttpResponseBadRequest("Invalid quantity.")
    if qty > sess.seats_remaining: return HttpResponseBadRequest("Not enough seats.")
    unit = sess.workshop.base_price; total = unit * qty
    pi = stripe.PaymentIntent.create(amount=int(total*100), currency="eur",
                                     metadata={"user_id": request.user.id, "session_id": sess.id, "qty": qty})
    booking = Booking.objects.create(user=request.user, session=sess, quantity=qty, unit_price=unit, total=total, stripe_pi=pi.id)
    return render(request, "checkout/pay.html", {"client_secret": pi.client_secret, "booking": booking, "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY})
