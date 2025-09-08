from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Workshop, Session, Review, Instructor
from .forms import WorkshopForm, SessionForm, ReviewForm

def home(request):
    return render(request, "workshops/home.html", {"workshops": Workshop.objects.filter(is_active=True)[:12]})

def detail(request, slug):
    w = get_object_or_404(Workshop, slug=slug, is_active=True)
    return render(request, "workshops/detail.html", {"w": w, "sessions": w.sessions.order_by("starts_at"), "reviews": w.reviews.select_related("user")[:20]})

def staff_only(u): return u.is_staff

@user_passes_test(staff_only)
def create_workshop(request):
    form = WorkshopForm(request.POST or None, request.FILES or None)
    if request.method=="POST" and form.is_valid():
        instr,_=Instructor.objects.get_or_create(user=request.user)
        obj=form.save(commit=False); obj.instructor=instr; obj.save()
        messages.success(request,"Workshop created.")
        return redirect("workshops:detail", slug=obj.slug)
    return render(request,"workshops/workshop_form.html",{"form":form, "page_title":"Create Workshop"})

@user_passes_test(staff_only)
def add_session(request, slug):
    w=get_object_or_404(Workshop, slug=slug)
    form=SessionForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        s=form.save(commit=False); s.workshop=w; s.save()
        messages.success(request,"Session added."); return redirect("workshops:detail", slug=w.slug)
    return render(request,"workshops/session_form.html",{"form":form,"w":w})

@login_required
def add_review(request, slug):
    w=get_object_or_404(Workshop, slug=slug, is_active=True)
    form=ReviewForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        Review.objects.update_or_create(workshop=w, user=request.user, defaults=form.cleaned_data)
        messages.success(request,"Review saved."); return redirect("workshops:detail", slug=w.slug)
    return render(request,"workshops/review_form.html",{"form":form,"w":w})

@login_required
def delete_review(request, review_id):
    r=get_object_or_404(Review, id=review_id, user=request.user)
    if request.method=="POST":
        slug=r.workshop.slug; r.delete(); messages.info(request,"Review deleted.")
        return redirect("workshops:detail", slug=slug)
    return render(request,"workshops/review_confirm_delete.html",{"review":r})
