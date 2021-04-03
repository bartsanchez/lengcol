from django.contrib import sitemaps

from definitions import models


class TermSitemap(sitemaps.Sitemap):
    changefreq = 'never'
    priority = 0.5

    def items(self):
        return models.Term.objects.all()

    def lastmod(self, obj):
        return obj.created
