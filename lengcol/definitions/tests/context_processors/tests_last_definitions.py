from django import test
from django.urls import reverse

from definitions import factories


class LastDefinitionsTests(test.TestCase):
    def setUp(self):
        self.client = test.Client()
        self.url = reverse('index')

    def test_hasnt_header_in_last_definitions(self):
        response = self.client.get(self.url)
        self.assertNotContains(response, 'Últimas definiciones')

    def test_has_header_in_last_definitions(self):
        factories.DefinitionFactory()
        response = self.client.get(self.url)
        self.assertContains(response, 'Últimas definiciones')

    def test_has_link_to_last_definition(self):
        definition = factories.DefinitionFactory(value="fake_definition")
        response = self.client.get(self.url)
        self.assertContains(
            response,
            '<a href="{}">fake_definition</a>'.format(
                definition.get_absolute_url()
            ),
            html=True
        )
