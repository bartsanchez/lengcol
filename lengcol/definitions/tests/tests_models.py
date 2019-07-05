from django import test

from base import models as base_models

from definitions import factories
from definitions import models


class TermTests(test.TestCase):
    def setUp(self):
        self.term = factories.TermFactory(value='my fake term')

    def test_str(self):
        self.assertEqual(str(self.term), 'my fake term')

    def test_inheritance(self):
        self.assertTrue(issubclass(models.Term, base_models.BaseModel))

    def test_slug(self):
        self.assertEqual(self.term.slug, 'my-fake-term')

    def test_definitions(self):
        definition_foo = factories.DefinitionFactory(term=self.term,
                                                     value='foo')
        definition_bar = factories.DefinitionFactory(term=self.term,
                                                     value='bar')
        factories.DefinitionFactory(value='qux')

        queryset = models.Definition.objects.filter(
            pk__in=[definition_foo.pk, definition_bar.pk]
        )
        self.assertQuerysetEqual(self.term.definitions,
                                 queryset,
                                 ordered=False,
                                 transform=lambda x: x)


class DefinitionTests(test.TestCase):
    def setUp(self):
        self.definition = factories.DefinitionFactory(value='my fake definition')

    def test_str(self):
        self.assertEqual(str(self.definition), 'my fake definition')

    def test_inheritance(self):
        self.assertTrue(issubclass(models.Definition, base_models.BaseModel))

    def test_has_examples(self):
        self.assertFalse(self.definition.has_examples)

        factories.ExampleFactory(definition=self.definition)

        self.assertTrue(self.definition.has_examples)

    def test_examples(self):
        example_foo = factories.ExampleFactory(definition=self.definition,
                                               value='foo')
        example_bar = factories.ExampleFactory(definition=self.definition,
                                               value='bar')
        factories.ExampleFactory(value='qux')

        queryset = models.Example.objects.filter(
            pk__in=[example_foo.pk, example_bar.pk]
        )
        self.assertQuerysetEqual(self.definition.examples,
                                 queryset,
                                 ordered=False,
                                 transform=lambda x: x)


class ExampleTests(test.TestCase):
    def setUp(self):
        self.example = factories.ExampleFactory(value='my fake example')

    def test_str(self):
        self.assertEqual(str(self.example), 'my fake example')
