from definitions import sitemaps
from django.contrib import admin
from django.contrib.sitemaps import views
from django.urls import include, path

from lengcol import views as lengcol_views

sitemaps_info = {
    "terms": sitemaps.TermSitemap,
    "definitions": sitemaps.DefinitionSitemap,
    "tags": sitemaps.TagSitemap,
    "static": sitemaps.StaticViewSitemap,
}
sitemap = {"sitemaps": sitemaps_info}

urlpatterns = [
    path("", include("definitions.urls")),
    path("", include("authentication.urls")),
    path("admin/", admin.site.urls),
    path("", include("django_prometheus.urls")),
    path("sitemap.xml", views.sitemap, sitemap, name="sitemap"),
    path("robots.txt", lengcol_views.RobotsTxtView.as_view(), name="robots-txt"),
]
