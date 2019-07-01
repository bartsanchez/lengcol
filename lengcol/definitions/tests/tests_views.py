from django import test
from django.urls import reverse
from django.utils import http

import splinter

from base import mixins

from definitions import factories
from definitions import models


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
            '<a class="nav-link" href="{}">Add new definition</a>'.format(
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


class DefinitionCreateViewTests(test.TestCase, mixins.W3ValidatorMixin):
    def setUp(self):
        self.client = test.Client()
        self.url = reverse('definition-add')

    def test_template_extends(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'lengcol/base.html')

    def test_redirects(self):
        self.assertEqual(models.Definition.objects.count(), 0)

        response = self.client.post(
            self.url,
            {'term': 'fake term', 'value': 'fake definition'},
        )

        definition = models.Definition.objects.get()

        self.assertRedirects(
            response,
            reverse('definition-detail', kwargs={'uuid': definition.uuid})
        )

    def test_add_new(self):
        self.assertEqual(models.Term.objects.count(), 0)
        self.assertEqual(models.Definition.objects.count(), 0)

        response = self.client.post(
            self.url,
            {'term': 'fake term', 'value': 'fake definition'},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(models.Term.objects.count(), 1)
        self.assertEqual(models.Definition.objects.count(), 1)

        self.assertEqual(
            models.Term.objects.first().value,
            'fake term',
        )
        self.assertEqual(
            models.Definition.objects.first().value,
            'fake definition',
        )

    def test_missing_term(self):
        self.assertEqual(models.Term.objects.count(), 0)
        self.assertEqual(models.Definition.objects.count(), 0)

        response = self.client.post(
            self.url,
            {'value': 'fake definition'},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(models.Term.objects.count(), 0)
        self.assertEqual(models.Definition.objects.count(), 0)

    def test_missing_value(self):
        self.assertEqual(models.Term.objects.count(), 0)
        self.assertEqual(models.Definition.objects.count(), 0)

        response = self.client.post(
            self.url,
            {'term': 'fake term'},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(models.Term.objects.count(), 1)
        self.assertEqual(models.Definition.objects.count(), 0)

        self.assertEqual(
            models.Term.objects.first().value,
            'fake term',
        )


class DefinitionDetailViewTests(test.TestCase, mixins.W3ValidatorMixin):
    def setUp(self):
        self.client = test.Client()
        self.term = factories.TermFactory(value='fake term')
        self.definition = factories.DefinitionFactory(term=self.term,
                                                      value='fake definition')
        self.url = reverse('definition-detail',
                           kwargs={'uuid': self.definition.uuid})

    def test_template_extends(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'lengcol/base.html')

    def test_term(self):
        response = self.client.get(self.url)

        self.assertContains(response, 'fake term')

    def test_definition(self):
        response = self.client.get(self.url)

        self.assertContains(response, 'fake definition')

    def test_creation_date(self):
        response = self.client.get(self.url)

        created = self.definition.created.strftime('%d-%m-%Y')

        self.assertContains(response, 'Fecha de creación {}'.format(created))

    def test_example_creation(self):
        response = self.client.get(self.url)

        self.assertNotContains(response, 'fake example 1')
        self.assertNotContains(response, 'fake example 2')

        response = self.client.post(
            self.url,
            {'example': 'fake example 1'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(models.Example.objects.count(), 1)

        self.assertContains(response, 'fake example 1')
        self.assertNotContains(response, 'fake example 2')

        response = self.client.post(
            self.url,
            {'example': 'fake example 2'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(models.Example.objects.count(), 2)

        self.assertContains(response, 'fake example 1')
        self.assertContains(response, 'fake example 2')

    def test_has_link_to_term_detail(self):
        response = self.client.get(self.url)

        self.assertContains(
            response,
            '<a href="{}">fake term</a>'.format(
                reverse('term-detail',
                        kwargs={'slug': self.definition.term.slug})
            ),
            html=True
        )


class TermDetailViewTests(test.TestCase, mixins.W3ValidatorMixin):
    def setUp(self):
        self.client = test.Client()
        self.term = factories.TermFactory(value='fake term')
        self.definition_foo = factories.DefinitionFactory(term=self.term,
                                                          value='foo')
        self.definition_bar = factories.DefinitionFactory(term=self.term,
                                                          value='bar')
        self.url = reverse('term-detail',
                           kwargs={'slug': self.term.slug})

    def test_template_extends(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'lengcol/base.html')

    def test_term(self):
        response = self.client.get(self.url)

        self.assertContains(response, 'fake term')

    def test_definitions(self):
        response = self.client.get(self.url)

        self.assertContains(response, 'foo')
        self.assertContains(response, 'bar')

    def test_has_link_to_definition_detail(self):
        response = self.client.get(self.url)

        self.assertContains(
            response,
            '<a href="{}">foo</a>'.format(
                reverse('definition-detail',
                        kwargs={'uuid': self.definition_foo.uuid})
            ),
            html=True
        )


class TermSearchViewTests(test.TestCase, mixins.W3ValidatorMixin):
    def setUp(self):
        self.client = test.Client()
        self.foo_term = factories.TermFactory(value='foo term')
        self.bar_term = factories.TermFactory(value='bar term')
        self.definition_foo = factories.DefinitionFactory(term=self.foo_term,
                                                          value='foo')
        self.definition_bar = factories.DefinitionFactory(term=self.bar_term,
                                                          value='bar')
        self.url = reverse('term-search')

    def test_template_extends(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'lengcol/base.html')

    def test_search(self):
        response = self.client.get(self.url)

        self.assertContains(response, 'foo term')
        self.assertContains(response, 'bar term')

    def test_search_foo(self):
        url = '{}?{}'.format(self.url, http.urlencode({'v': 'foo'}))
        response = self.client.get(url)

        self.assertContains(response, 'foo term')
        self.assertNotContains(response, 'bar term')

    def test_search_bar(self):
        url = '{}?{}'.format(self.url, http.urlencode({'v': 'bar'}))
        response = self.client.get(url)

        self.assertContains(response, 'bar term')
        self.assertNotContains(response, 'foo term')
