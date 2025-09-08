from django.shortcuts import render
from django.http import HttpResponse
def robots_txt(_): return HttpResponse("User-agent: *\nDisallow:\nSitemap: /sitemap.xml\n", content_type="text/plain")
def custom_404(request, exception): return render(request, "core/404.html", status=404)
