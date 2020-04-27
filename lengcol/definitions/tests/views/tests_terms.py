import freezegun
from django import test
from django.urls import reverse
from django.utils import http

from base import mixins
from definitions import factories


@freezegun.freeze_time('2020-01-01')
class TermDetailViewTests(test.TestCase, mixins.W3ValidatorMixin):
    def setUp(self):
        self.client = test.Client()
        self.term = factories.TermFactory(value='fake term')
        self.definition_foo = factories.DefinitionFactory(
            uuid='cb8d30f8-b60a-46e8-9cad-f3d5ff28d269',
            term=self.term,
            value='foo',
        )
        self.definition_bar = factories.DefinitionFactory(
            uuid='75484634-4f96-4bc9-8d94-bfe8523ba7cd',
            term=self.term,
            value='bar',
        )
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
            f'<a href="{self.definition_foo.get_absolute_url()}">foo</a>',
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
        self.definition_foo = factories.DefinitionFactory(
            uuid='b3ec0487-d422-4d0e-86c0-0b80402fb012',
            term=self.foo_term,
            value='foo',
        )
        self.definition_bar = factories.DefinitionFactory(
            uuid='8ce7d087-b231-4562-b43f-dd27c7af7eba',
            term=self.bar_term,
            value='bar',
        )
        self.url = reverse('term-search')

    def test_template_extends(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'lengcol/base.html')

    def get_html_link(self, obj):
        return '<a href="{}">{}</a>'.format(obj.get_absolute_url(), obj.value)

    def test_search(self):
        response = self.client.get(self.url)

        self.assertContains(
            response, self.get_html_link(self.foo_term), html=True
        )
        self.assertContains(
            response, self.get_html_link(self.bar_term), html=True
        )

    def test_search_foo(self):
        url = '{}?{}'.format(self.url, http.urlencode({'v': 'foo'}))
        response = self.client.get(url)

        self.assertContains(
            response, self.get_html_link(self.foo_term), html=True
        )
        self.assertNotContains(
            response, self.get_html_link(self.bar_term), html=True
        )

    def test_search_bar(self):
        url = '{}?{}'.format(self.url, http.urlencode({'v': 'bar'}))
        response = self.client.get(url)

        self.assertContains(
            response, self.get_html_link(self.bar_term), html=True
        )
        self.assertNotContains(
            response, self.get_html_link(self.foo_term), html=True
        )
