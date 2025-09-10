from django.urls import path
from . import views, webhooks
app_name="checkout"
urlpatterns = [
    path("start/<int:session_id>/", views.start_checkout, name="start"),
    path("webhook/", webhooks.stripe_webhook, name="webhook"),
    path("success/<int:booking_id>/", views.success, name="success"),
]
