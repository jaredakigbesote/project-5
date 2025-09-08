from django.db import models
class NewsletterSubscriber(models.Model):
    email=models.EmailField(unique=True)
    joined=models.DateTimeField(auto_now_add=True)
    source=models.CharField(max_length=40, default="on-site")
    def __str__(self): return self.email
