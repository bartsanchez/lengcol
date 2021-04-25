from django import test

from definitions import forms, models


class ModelChoiceFieldAsTextTests(test.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.model_choice_field = forms.ModelChoiceFieldAsText(
            queryset=models.Definition.objects.all(),
            field='value',
        )

    def test_widget(self):
        self.assertIn(
            'TextInput',
            str(self.model_choice_field.widget),
        )


class DefinitionFormTests(test.TestCase):
    @classmethod
    def setUpTestData(cls):
        data = {
            'term': 'this is a fake term',
            'value': 'this is a fake definition',
        }
        cls.form = forms.DefinitionForm(data=data)

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

    def test_active_field_is_not_included(self):
        f = forms.DefinitionForm()

        self.assertNotIn('active', f.fields)
