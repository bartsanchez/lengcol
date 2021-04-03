from django import test
from django.urls import reverse

from definitions import factories


class TermSitemapViewTests(test.TestCase):
    def test_has_term(self):
        term = factories.TermFactory(value='fake term')

        response = self.client.get(reverse('sitemap'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, term.get_absolute_url())
