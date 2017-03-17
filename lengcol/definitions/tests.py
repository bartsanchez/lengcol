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


class IndexViewTests(test.TestCase):
    def setUp(self):
        self.client = test.Client()

    def test_template_extends(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'lengcol/base.html')

    def test_title(self):
        response = self.client.get('/')

        self.assertContains(response, '<h1>Lenguaje coloquial</h1>', html=True)
