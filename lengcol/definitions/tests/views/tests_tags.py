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

    @classmethod
    def setUpTestData(cls):
        factories.DefinitionFactory(tags='a fake tag, othertag')
        cls.client = test.Client()
        cls.url = reverse('tag-list')

    def test_template_extends(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'lengcol/base.html')

    def test_tags_entries(self):
        response = self.client.get(self.url)

        tag_html = (
            '<li class="list-group-item"><a href="{}">{}</a></li>'
        )
        for tag in ('a fake tag', 'othertag'):
            href_url = reverse('definitions-by-tag', kwargs={'tag_name': tag})
            self.assertContains(
                response,
                tag_html.format(href_url, tag),
                html=True
            )

    def test_has_link_to_tags(self):
        response = self.client.get(self.url)

        tag_html = (
            '<a href="{}" data-weight="1">{}</a>'
        )
        for tag in ('a fake tag', 'othertag'):
            href_url = reverse('definitions-by-tag', kwargs={'tag_name': tag})
            self.assertContains(
                response,
                tag_html.format(href_url, tag),
                html=True
            )
