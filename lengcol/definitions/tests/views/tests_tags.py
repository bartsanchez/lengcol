from django import test
from django.urls import reverse

from base import mixins
from definitions import factories


class TagListViewTests(test.TestCase,
                       mixins.W3ValidatorMixin,
                       mixins.HTMLValidatorMixin,
                       mixins.MetaDescriptionValidatorMixin):
    page_title = 'Lenguaje Coloquial | Diccionario en español'
    h1_header = 'Etiquetas'
    meta_description = (
        'Etiquetas asignadas a definiciones, creadas por usuarios de esta '
        'página, de expresiones usadas de manera coloquial.'
    )

    def setUp(self):
        factories.DefinitionFactory(tags='a fake tag, othertag')
        self.client = test.Client()
        self.url = reverse('tag-list')

    def test_template_extends(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'lengcol/base.html')

    def test_tags_entries(self):
        response = self.client.get(self.url)

        self.assertContains(
            response,
            '<li class="list-group-item">a fake tag</li>',
            html=True
        )
        self.assertContains(
            response,
            '<li class="list-group-item">othertag</li>',
            html=True
        )
