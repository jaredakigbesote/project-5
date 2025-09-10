from django.db import models
from django.conf import settings
from django.db.models import F
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.utils import timezone

class WorkshopCategory(models.Model):
    name=models.CharField(max_length=80, unique=True)
    slug=models.SlugField(max_length=90, unique=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self): return self.name

class Instructor(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio=models.TextField(blank=True); website=models.URLField(blank=True)
    def __str__(self): return self.user.get_full_name() or self.user.username

class Workshop(models.Model):
    category=models.ForeignKey(WorkshopCategory,on_delete=models.PROTECT,related_name="workshops")
    title=models.CharField(max_length=150)
    slug=models.SlugField(max_length=170, unique=True, blank=True)
    instructor=models.ForeignKey(Instructor,on_delete=models.PROTECT,related_name="workshops")
    short_description=models.CharField(max_length=200)
    description=models.TextField()
    base_price=models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    image=models.ImageField(upload_to="workshops/", blank=True)
    is_active=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=["-created"]
    def save(self,*a,**k):
        if not self.slug: self.slug=slugify(f"{self.title}-{self.instructor_id}"); super().save(*a,**k)
    def __str__(self): return self.title

class Session(models.Model):
    workshop=models.ForeignKey(Workshop,on_delete=models.CASCADE, related_name="sessions")
    starts_at=models.DateTimeField(); 
    ends_at=models.DateTimeField()
    capacity=models.PositiveIntegerField(default=12)
    seats_sold=models.PositiveIntegerField(default=0)
    location=models.CharField(max_length=180)
    @property
    def seats_remaining(self):
        return max(0, self.capacity - self.seats_sold)


    def __str__(self):
        return f"{self.workshop.title} @ {self.starts_at:%Y-%m-%d %H:%M}"


class Review(models.Model):
    workshop=models.ForeignKey(Workshop,on_delete=models.CASCADE,related_name="reviews")
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    rating=models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment=models.TextField(blank=True)
    created=models.DateTimeField(auto_now_add=True)
    class Meta: unique_together=("workshop","user"); ordering=["-created"]
    def __str__(self): return f"{self.workshop} ★{self.rating}"