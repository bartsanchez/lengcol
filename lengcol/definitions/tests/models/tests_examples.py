from definitions import factories
from django import test


class ExampleTests(test.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.example = factories.ExampleFactory(value="my fake example")

    def test_str(self):
        self.assertEqual(str(self.example), "my fake example")
