from base import mixins
from definitions import factories
from django import test
from django.urls import reverse
from django.utils import http


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

    def test_has_link_to_definition_detail(self):
        response = self.client.get(self.url)

        self.assertContains(
            response,
            '<a href="{}">foo</a>'.format(
                reverse('definition-detail',
                        kwargs={'uuid': self.definition_foo.uuid})
            ),
            html=True
        )

    def test_has_examples(self):
        response = self.client.get(self.url)

        self.assertNotContains(response, 'fake example')

        factories.ExampleFactory(definition=self.definition_foo,
                                 value='fake example')

        response = self.client.get(self.url)

        self.assertContains(response, 'fake example')


class TermSearchViewTests(test.TestCase, mixins.W3ValidatorMixin):
    def setUp(self):
        self.client = test.Client()
        self.foo_term = factories.TermFactory(value='foo term')
        self.bar_term = factories.TermFactory(value='bar term')
        self.definition_foo = factories.DefinitionFactory(term=self.foo_term,
                                                          value='foo')
        self.definition_bar = factories.DefinitionFactory(term=self.bar_term,
                                                          value='bar')
        self.url = reverse('term-search')

    def test_template_extends(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'lengcol/base.html')

    def test_search(self):
        response = self.client.get(self.url)

        self.assertContains(response, 'foo term')
        self.assertContains(response, 'bar term')

    def test_search_foo(self):
        url = '{}?{}'.format(self.url, http.urlencode({'v': 'foo'}))
        response = self.client.get(url)

        self.assertContains(response, 'foo term')
        self.assertNotContains(response, 'bar term')

    def test_search_bar(self):
        url = '{}?{}'.format(self.url, http.urlencode({'v': 'bar'}))
        response = self.client.get(url)

        self.assertContains(response, 'bar term')
        self.assertNotContains(response, 'foo term')
