from definitions import factories
from django import test


class ExampleTests(test.TestCase):
    def setUp(self):
        self.example = factories.ExampleFactory(value='my fake example')

    def test_str(self):
        self.assertEqual(str(self.example), 'my fake example')
