from django.urls import path
from . import views

app_name="workshops"

urlpatterns=[
    path("", views.home, name="home"),
    
    path("w/new/", views.create_workshop, name="create"),
    path("w/<slug:slug>/session/add/", views.add_session, name="add_session"),
    path("w/<slug:slug>/review/", views.add_review, name="add_review"),
    path("reviews/<int:review_id>/delete/", views.delete_review, name="delete_review"),


     path("w/<slug:slug>/", views.detail, name="detail"),
]
