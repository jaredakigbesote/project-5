from django.contrib import admin
from .models import WorkshopCategory, Instructor, Workshop, Session, Review

@admin.register(WorkshopCategory)
class WorkshopCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("user", "website")
    search_fields = ("user__username", "user__email")


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "instructor", "base_price", "is_active", "created")
    list_filter = ("is_active", "category")
    search_fields = ("title", "short_description")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("workshop", "starts_at", "ends_at", "capacity", "seats_sold", "location")
    list_filter = ("workshop", "starts_at")
    search_fields = ("workshop__title", "location")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("workshop", "user", "rating", "created")
    list_filter = ("rating", "created")
    search_fields = ("workshop__title", "user__username", "comment")