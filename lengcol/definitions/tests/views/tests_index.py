import freezegun
import splinter
from django import test
from django.conf import settings
from django.urls import reverse

from base import mixins
from definitions import factories


@freezegun.freeze_time('2020-01-01')
class IndexViewTests(test.TestCase, mixins.W3ValidatorMixin):
    def setUp(self):
        factories.DefinitionFactory(
            uuid='13bf0f68-eeb2-4777-a739-6ee5be30bacc',
            value='fake_definition',
        )
        self.client = test.Client()
        self.url = reverse('index')

    def test_template_extends(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'lengcol/base.html')

    def test_title(self):
        response = self.client.get(self.url)

        self.assertContains(
            response,
            '<a class="navbar-brand" href="/">Lenguaje coloquial</a>',
            html=True
        )

    def test_has_link_to_term_detail(self):
        term = factories.TermFactory(value='my fake term')
        factories.DefinitionFactory(term=term, value='fake definition')
        response = self.client.get(self.url)

        self.assertContains(
            response,
            f'<a href="{term.get_absolute_url()}">my fake term</a>',
            html=True
        )

    def test_has_link_to_add_new_definition(self):
        response = self.client.get(self.url)

        linked_url = reverse('definition-add')
        self.assertContains(
            response,
            '<a class="nav-link" href="{}">Añadir definición</a>'.format(
                linked_url
            ),
            html=True
        )

    def test_has_link_to_definition_detail(self):
        definition = factories.DefinitionFactory(value='fake definition')

        response = self.client.get(self.url)

        self.assertContains(
            response,
            f'<a href="{definition.get_absolute_url()}">&#128279;</a>',
            html=True
        )

    def test_term_search_form_is_working(self):
        foo_term = factories.TermFactory(value='foo term')
        bar_term = factories.TermFactory(value='bar term')
        factories.DefinitionFactory(term=foo_term, value='foo')
        factories.DefinitionFactory(term=bar_term, value='bar')
        foo_term_html = '<a href="{}">foo term</a>'.format(
            foo_term.get_absolute_url()
        )
        bar_term_html = '<a href="{}">bar term</a>'.format(
            bar_term.get_absolute_url()
        )
        with splinter.Browser('django') as browser:
            browser.visit(self.url)

            self.assertIn(foo_term_html, browser.html)
            self.assertIn(bar_term_html, browser.html)

            browser.fill('v', 'f')
            browser.find_by_id('form-button').click()

            self.assertEqual(browser.url, reverse('term-search'))
            self.assertIn(foo_term_html, browser.html)
            self.assertNotIn(bar_term_html, browser.html)

    def test_has_examples(self):
        definition = factories.DefinitionFactory(value='fake definition')

        response = self.client.get(self.url)

        self.assertNotContains(response, 'fake example')

        factories.ExampleFactory(definition=definition, value='fake example')

        response = self.client.get(self.url)

        self.assertContains(response, 'fake example')

    def test_has_email_contact_link(self):
        response = self.client.get(self.url)

        email_link = settings.APP_EMAIL
        self.assertContains(
            response,
            '<a href="mailto:{0}">{0}</a>'.format(email_link),
            html=True
        )

    def test_inactive_definitions_does_not_appear(self):
        definition = factories.DefinitionFactory(value='fake definition')

        response = self.client.get(self.url)

        self.assertContains(response, 'fake definition')

        definition.active = False
        definition.save()

        response = self.client.get(self.url)

        self.assertNotContains(response, 'fake definition')
