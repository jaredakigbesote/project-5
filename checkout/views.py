from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.db import transaction
from django.db.models import F
import stripe
from bookings.models import Booking
from workshops.models import Session

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def start_checkout(request, session_id):
    if request.method != "POST":
        # Someone hit the URL directly; redirect back to the session page.
        return redirect("workshops:detail", slug=get_object_or_404(Session, pk=session_id).workshop.slug)


    stripe.api_key = settings.STRIPE_SECRET_KEY or ""

    sess = get_object_or_404(Session, pk=session_id, workshop__is_active=True)
    try:
        qty = int(request.POST.get("quantity", 1))
    except ValueError:
        return HttpResponseBadRequest("Invalid quantity.")

    if qty < 1:
        return HttpResponseBadRequest("Invalid quantity.")
    if qty > sess.seats_remaining:
        return HttpResponseBadRequest("Not enough seats.")

    unit = sess.workshop.base_price
    total = unit * qty

    # Create the PaymentIntent
    pi = stripe.PaymentIntent.create(
        amount=int(total * 100),
        currency="eur",
        automatic_payment_methods={"enabled": True},
        metadata={"user_id": request.user.id, "session_id": sess.id, "qty": qty},
    )

    booking = Booking.objects.create(
        user=request.user,
        session=sess,
        quantity=qty,
        unit_price=unit,
        total=total,
        stripe_pi=pi.id,
    )
    return render(
        request,
        "checkout/pay.html",
        {
            "client_secret": pi.client_secret,                    
            "booking": booking,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,      
        },
    )

@login_required
def success(request, booking_id):
     booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
     return render(request, "checkout/success.html", {"booking": booking})

if pi.status == "succeeded" and not booking.paid:
        with transaction.atomic():
            b = Booking.objects.select_for_update().get(pk=booking.pk)
            if not b.paid:
                # Increment seats sold atomically
                Session.objects.filter(pk=b.session_id).update(
                    seats_sold=F("seats_sold") + b.quantity
                )
                b.paid = True
                b.save(update_fields=["paid"])
