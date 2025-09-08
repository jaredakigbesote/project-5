from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import stripe
from bookings.models import Booking

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig = request.META.get("HTTP_STRIPE_SIGNATURE")
    try:
        event = stripe.Webhook.construct_event(payload, sig, settings.STRIPE_WEBHOOK_SECRET)
    except Exception:
        return HttpResponse(status=400)

    if event.get("type") == "payment_intent.succeeded":
        pi = event["data"]["object"]
        with transaction.atomic():
            booking = Booking.objects.select_for_update().get(stripe_pi=pi["id"])
            if not booking.paid:
                booking.paid = True; booking.save()
                s = booking.session
                if booking.quantity > s.seats_remaining: raise Exception("Oversell")
                s.seats_sold += booking.quantity; s.save()
    return HttpResponse(status=200)
