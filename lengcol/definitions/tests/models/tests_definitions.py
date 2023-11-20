from base import models as base_models
from definitions import factories, models
from django import test


class DefinitionTests(test.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.definition = factories.DefinitionFactory(
            value='my fake definition'
        )

    def test_str(self):
        self.assertEqual(str(self.definition), 'my fake definition')

    def test_inheritance(self):
        self.assertTrue(issubclass(models.Definition, base_models.BaseModel))

    def test_ordering(self):
        def1 = factories.DefinitionFactory(value='definition_1')
        def2 = factories.DefinitionFactory(value='definition_2')
        def3 = factories.DefinitionFactory(value='definition_3')

        self.assertEqual(
            list(models.Definition.objects.all()),
            [self.definition, def1, def2, def3]
        )

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
                                 ordered=False)
