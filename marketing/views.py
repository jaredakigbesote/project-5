from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import NewsletterSubscriberForm
def subscribe(request):
    form = NewsletterSubscriberForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        form.save(); messages.success(request,"Thanks for subscribing!"); return redirect("workshops:home")
    return render(request,"marketing/subscribe.html",{"form":form})
