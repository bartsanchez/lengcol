from django import test
from django.urls import reverse

from base import mixins

from definitions import factories
from definitions import models


class IndexViewTests(test.TestCase, mixins.W3ValidatorMixin):
    def setUp(self):
        self.client = test.Client()
        self.url = '/'

    def test_template_extends(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'lengcol/base.html')

    def test_title(self):
        response = self.client.get(self.url)

        self.assertContains(response, '<h1>Lenguaje coloquial</h1>', html=True)

    def test_has_link_to_term_detail(self):
        term = factories.TermFactory(value='my fake term')

        response = self.client.get(self.url)

        self.assertContains(
            response,
            '<a href="{}">my fake term</a>'.format(
                reverse('term-detail', kwargs={'slug': term.slug})
            ),
            html=True
        )

    def test_has_link_to_add_new_definition(self):
        response = self.client.get(self.url)

        linked_url = reverse('definition-add')
        self.assertContains(
            response,
            '<a href="{}">Add new definition</a>'.format(linked_url),
            html=True
        )

    def test_has_link_to_definition_detail(self):
        definition = factories.DefinitionFactory(value='fake definition')

        response = self.client.get(self.url)

        self.assertContains(
            response,
            '<a href="{}">fake definition</a>'.format(
                reverse('definition-detail', kwargs={'pk': definition.pk})
            ),
            html=True
        )


class DefinitionCreateViewTests(test.TestCase, mixins.W3ValidatorMixin):
    def setUp(self):
        self.client = test.Client()
        self.url = reverse('definition-add')

    def test_template_extends(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'lengcol/base.html')

    def test_redirects(self):
        response = self.client.post(
            self.url,
            {'term': 'fake term', 'value': 'fake definition'},
        )

        self.assertRedirects(response, '/')

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
                           kwargs={'pk': self.definition.pk})

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

        self.assertContains(response, 'Created at {}'.format(created))


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
