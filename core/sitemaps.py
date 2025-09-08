from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from workshops.models import Workshop
class WorkshopSitemap(Sitemap):
    changefreq="weekly"; priority=0.7
    def items(self): return Workshop.objects.filter(is_active=True)
    def location(self,obj): return reverse("workshops:detail", args=[obj.slug])
    def lastmod(self,obj): return obj.created