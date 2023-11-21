from definitions import factories
from django import test
from django.urls import reverse


class LastTermsTests(test.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = test.Client()
        cls.url = reverse("index")

    def test_hasnt_header_in_last_terms(self):
        response = self.client.get(self.url)
        self.assertNotContains(response, "Últimas definiciones")

    def test_has_header_in_last_terms(self):
        factories.TermFactory()
        response = self.client.get(self.url)
        self.assertContains(response, "Últimas definiciones")

    def test_has_link_to_last_term(self):
        term = factories.TermFactory(value="fake_term")
        response = self.client.get(self.url)
        self.assertContains(
            response,
            '<li><a class="last-terms" href="{}">fake_term</a></li>'.format(
                term.get_absolute_url()
            ),
            html=True,
        )
