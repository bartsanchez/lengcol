from django import test

from base import models as base_models
from definitions import factories, models


class TermTests(test.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.term = factories.TermFactory(value='my fake term')

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
