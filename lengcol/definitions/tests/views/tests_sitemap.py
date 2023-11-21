from definitions import factories, sitemaps
from django import test
from django.urls import reverse


class TermSitemapViewTests(test.TestCase):
    def test_has_term(self):
        term = factories.TermFactory(value="fake term")

        response = self.client.get(reverse("sitemap"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, term.get_absolute_url())

    def test_has_definition(self):
        definition = factories.DefinitionFactory(value="fake definition")

        response = self.client.get(reverse("sitemap"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, definition.get_absolute_url())

    def test_has_tags(self):
        factories.DefinitionFactory(value="fake definition", tags="tag1, tag3")

        response = self.client.get(reverse("sitemap"))

        self.assertEqual(response.status_code, 200)

        for tag in ("tag1", "tag3"):
            self.assertContains(
                response, reverse("definitions-by-tag", kwargs={"tag_name": tag})
            )

    def test_has_statics(self):
        static_view_sitemap = sitemaps.StaticViewSitemap()
        static_page_names = static_view_sitemap.items()

        response = self.client.get(reverse("sitemap"))

        self.assertEqual(response.status_code, 200)

        for static_page_name in static_page_names:
            self.assertContains(response, reverse(static_page_name))
