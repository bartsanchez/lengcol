from django import test

from definitions import factories


class TermTests(test.TestCase):
    def test_str(self):
        term = factories.TermFactory(value='my fake term')

        self.assertEqual(str(term), 'my fake term')


class DefinitionTests(test.TestCase):
    def test_str(self):
        definition = factories.DefinitionFactory(value='my fake definition')

        self.assertEqual(str(definition), 'my fake definition')
