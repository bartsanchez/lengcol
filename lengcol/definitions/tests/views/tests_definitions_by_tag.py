import freezegun
from django import test
from django.urls import reverse

from base import mixins
from definitions import factories


@freezegun.freeze_time('2020-01-01')
class DefinitionsByTagViewTests(test.TestCase,
                                mixins.W3ValidatorMixin,
                                mixins.HTMLValidatorMixin,
                                mixins.MetaDescriptionValidatorMixin):
    page_title = 'Lenguaje Coloquial | Diccionario en español'
    h1_header = 'Definiciones con la etiqueta fake_tag'
    meta_description = 'Definiciones que incluyen la etiqueta fake_tag.'

    def setUp(self):
        factories.DefinitionFactory(
            uuid='13bf0f68-eeb2-4777-a739-6ee5be30bacc',
            value='fake_definition',
            tags='one tag, fake_tag   , another tag',
        )
        self.client = test.Client()
        self.url = reverse('definitions-by-tag',
                           kwargs={'tag_name': 'fake_tag'})

    def test_template_extends(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'definitions/by_tag.html')

    def test_title(self):
        response = self.client.get(self.url)

        self.assertContains(
            response,
            '<a class="navbar-brand" href="/">Lenguaje coloquial</a>',
            html=True
        )

    def test_definition_for_existing_tag(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'fake_definition')
        self.assertContains(response, 'fake_tag')

    def test_non_existing_tag(self):
        self.url = reverse('definitions-by-tag',
                           kwargs={'tag_name': 'non existing tag'})

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)
