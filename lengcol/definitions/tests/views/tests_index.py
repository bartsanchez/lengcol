import splinter
from django import test
from django.urls import reverse

from base import mixins
from definitions import factories


class IndexViewTests(test.TestCase, mixins.W3ValidatorMixin):
    def setUp(self):
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
        definition = factories.DefinitionFactory(term=term,
                                                 value='fake definition')
        response = self.client.get(self.url)

        self.assertContains(
            response,
            '<a href="{}">my fake term</a>'.format(
                reverse('term-detail', kwargs={'slug': definition.term.slug})
            ),
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
            '<a href="{}">fake definition</a>'.format(
                reverse('definition-detail', kwargs={'uuid': definition.uuid})
            ),
            html=True
        )

    def test_term_search_form_is_working(self):
        foo_term = factories.TermFactory(value='foo term')
        bar_term = factories.TermFactory(value='bar term')
        factories.DefinitionFactory(term=foo_term, value='foo')
        factories.DefinitionFactory(term=bar_term, value='bar')

        with splinter.Browser('django') as browser:
            browser.visit(self.url)

            self.assertIn('foo term', browser.html)
            self.assertIn('bar term', browser.html)

            browser.fill('v', 'f')
            browser.find_by_id('form-button').click()

            self.assertEqual(browser.url, reverse('term-search'))
            self.assertIn('foo term', browser.html)
            self.assertNotIn('bar term', browser.html)

    def test_has_examples(self):
        definition = factories.DefinitionFactory(value='fake definition')

        response = self.client.get(self.url)

        self.assertNotContains(response, 'fake example')

        factories.ExampleFactory(definition=definition, value='fake example')

        response = self.client.get(self.url)

        self.assertContains(response, 'fake example')

    def test_has_email_contact_link(self):
        response = self.client.get(self.url)

        email_link = 'info@lenguajecoloquial.com'
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
