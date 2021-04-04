from django.contrib import admin
from django.contrib.sitemaps import views
from django.urls import include, path

from definitions import sitemaps

sitemaps_info = {
    'terms': sitemaps.TermSitemap,
    'definitions': sitemaps.DefinitionSitemap,
}
sitemap = {'sitemaps': sitemaps_info}

urlpatterns = [
    path('', include('definitions.urls')),
    path('', include('authentication.urls')),
    path('admin/', admin.site.urls),
    path('', include('django_prometheus.urls')),
    path('sitemap.xml', views.sitemap, sitemap, name='sitemap')
]
