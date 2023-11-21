from definitions import models
from django.contrib import sitemaps
from django.urls import reverse
from tagging import models as tagging_models


class TermSitemap(sitemaps.Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return models.Term.objects.all()

    def lastmod(self, obj):
        return obj.created


class DefinitionSitemap(sitemaps.Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return models.Definition.objects.all()

    def lastmod(self, obj):
        return obj.created


class TagSitemap(sitemaps.Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return tagging_models.Tag.objects.all()

    def location(self, item):
        return reverse("definitions-by-tag", kwargs={"tag_name": item})


class StaticViewSitemap(sitemaps.Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return ["tag-list", "term-search", "definition-add"]

    def location(self, item):
        return reverse(item)
