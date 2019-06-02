from django import test
from django.urls import reverse

from definitions import factories
from definitions import forms
from definitions import models


class TermTests(test.TestCase):
    def test_str(self):
        term = factories.TermFactory(value='my fake term')

        self.assertEqual(str(term), 'my fake term')


class DefinitionTests(test.TestCase):
    def test_str(self):
        definition = factories.DefinitionFactory(value='my fake definition')

        self.assertEqual(str(definition), 'my fake definition')


class IndexViewTests(test.TestCase):
    def setUp(self):
        self.client = test.Client()

    def test_template_extends(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'lengcol/base.html')

    def test_title(self):
        response = self.client.get('/')

        self.assertContains(response, '<h1>Lenguaje coloquial</h1>', html=True)

    def test_has_link_to_add_new_definition(self):
        response = self.client.get('/')

        self.assertContains(
            response,
            '<a href="{}">Add new definition</a>'.format(reverse('add')),
            html=True
        )


class ModelChoiceFieldAsTextTests(test.TestCase):
    def setUp(self):
        self.model_choice_field = forms.ModelChoiceFieldAsText(
            queryset=models.Definition.objects.all(),
            field='value',
        )

    def test_widget(self):
        self.assertIn(
            'TextInput',
            str(self.model_choice_field.widget),
        )


class DefinitionFormTests(test.TestCase):
    def setUp(self):
        data = {
            'term': 'this is a fake term',
            'value': 'this is a fake definition',
        }
        self.form = forms.DefinitionForm(data=data)

    def test_form_is_valid(self):
        self.assertTrue(self.form.is_valid())

    def test_missing_term(self):
        data = {
            'value': 'this is a fake definition',
        }
        form = forms.DefinitionForm(data=data)

        self.assertFalse(form.is_valid())

    def test_missing_value(self):
        data = {
            'term': 'this is a fake term',
        }
        form = forms.DefinitionForm(data=data)

        self.assertFalse(form.is_valid())

    def test_object_created(self):
        self.assertEqual(models.Definition.objects.count(), 0)

        self.form.save()

        self.assertEqual(models.Definition.objects.count(), 1)


class DefinitionCreateViewTests(test.TestCase):
    def setUp(self):
        self.client = test.Client()
        self.url = reverse('add')

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


class DefinitionDetailViewTests(test.TestCase):
    def setUp(self):
        self.client = test.Client()
        self.term = factories.TermFactory(value='fake term')
        self.definition = factories.DefinitionFactory(term=self.term,
                                                      value='fake definition')
        self.url = reverse('detail', kwargs={'pk': self.definition.pk})

    def test_template_extends(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'definitions/definition_detail.html')

    def test_term(self):
        response = self.client.get('/')

        self.assertContains(response, 'fake term', html=True)

    def test_definition(self):
        response = self.client.get('/')

        self.assertContains(response, 'fake definition', html=True)
