from unittest import mock

import freezegun
from base import mixins
from django import test
from django.urls import reverse
from django.utils import http

from definitions import factories, views


@freezegun.freeze_time("2020-01-01")
class TermDetailViewTests(
    test.TestCase,
    mixins.W3ValidatorMixin,
    mixins.HTMLValidatorMixin,
    mixins.MetaDescriptionValidatorMixin,
):
    page_title = "Lenguaje Coloquial | Definiciones de fake term"
    h1_header = "Definición de fake term"
    meta_description = (
        "Significados y ejemplos en español de la palabra o expresión "
        "coloquial fake term."
    )

    @classmethod
    def setUpTestData(cls):
        cls.client = test.Client()
        cls.term = factories.TermFactory(value="fake term")
        cls.definition_foo = factories.DefinitionFactory(
            uuid="cb8d30f8-b60a-46e8-9cad-f3d5ff28d269",
            term=cls.term,
            value="foo",
        )
        cls.definition_bar = factories.DefinitionFactory(
            uuid="75484634-4f96-4bc9-8d94-bfe8523ba7cd",
            term=cls.term,
            value="bar",
        )
        cls.url = reverse("term-detail", kwargs={"slug": cls.term.slug})

    def test_template_extends(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, "lengcol/base.html")

    def test_term(self):
        response = self.client.get(self.url)

        self.assertContains(response, "fake term")

    def test_definitions(self):
        response = self.client.get(self.url)

        self.assertContains(response, "foo")
        self.assertContains(response, "bar")

    def test_has_link_to_definition_detail(self):
        response = self.client.get(self.url)

        definition = self.definition_foo
        self.assertContains(
            response,
            f'<a href="{definition.get_absolute_url()}">&#128279;</a>',
            html=True,
        )

    def test_has_examples(self):
        response = self.client.get(self.url)

        self.assertNotContains(response, "fake example")

        factories.ExampleFactory(definition=self.definition_foo, value="fake example")

        response = self.client.get(self.url)

        self.assertContains(response, "fake example")


@freezegun.freeze_time("2020-01-01")
class TermSearchViewTests(
    test.TestCase,
    mixins.W3ValidatorMixin,
    mixins.HTMLValidatorMixin,
    mixins.MetaDescriptionValidatorMixin,
):
    page_title = "Lenguaje Coloquial | Diccionario en español"
    h1_header = "Resultados de la búsqueda"
    meta_description = (
        "Resultados de una búsqueda de definición para el "
        "proyecto Lenguaje Coloquial."
    )

    @classmethod
    def setUpTestData(cls):
        cls.client = test.Client()
        cls.foo_term = factories.TermFactory(value="foo term")
        cls.bar_term = factories.TermFactory(value="bar term")
        cls.definition_foo = factories.DefinitionFactory(
            uuid="b3ec0487-d422-4d0e-86c0-0b80402fb012",
            term=cls.foo_term,
            value="foo",
        )
        cls.definition_bar = factories.DefinitionFactory(
            uuid="8ce7d087-b231-4562-b43f-dd27c7af7eba",
            term=cls.bar_term,
            value="bar",
        )
        cls.url = reverse("term-search")

    def test_template_extends(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, "lengcol/base.html")

    def get_html_link(self, obj):
        return f'<a href="{obj.get_absolute_url()}">{obj.value}</a>'

    def test_search(self):
        response = self.client.get(self.url)

        self.assertContains(response, self.get_html_link(self.foo_term), html=True)
        self.assertContains(response, self.get_html_link(self.bar_term), html=True)

    def test_search_foo(self):
        url = "{}?{}".format(self.url, http.urlencode({"v": "foo"}))
        response = self.client.get(url)

        self.assertContains(response, self.get_html_link(self.foo_term), html=True)
        self.assertNotContains(response, self.get_html_link(self.bar_term), html=True)

    def test_search_bar(self):
        url = "{}?{}".format(self.url, http.urlencode({"v": "bar"}))
        response = self.client.get(url)

        self.assertContains(response, self.get_html_link(self.bar_term), html=True)
        self.assertNotContains(response, self.get_html_link(self.foo_term), html=True)

    @mock.patch("definitions.models.Term.objects.annotate")
    @mock.patch(
        "definitions.views.TermSearchView.db_engine_is_sqlite",
        return_value=False,
    )
    def test_search_postgresql_engine(self, db_check_mock, annotate_mock):
        url = "{}?{}".format(self.url, http.urlencode({"v": "bar"}))
        self.client.get(url)

        db_check_mock.assert_called_once_with()
        annotate_mock.assert_called_once()

    def test_db_engine_is_sqlite(self):
        self.assertTrue(views.TermSearchView().db_engine_is_sqlite())


class TermSearchViewPaginationTests(test.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = test.Client()
        cls.url = reverse("term-search")

    def test_do_have_link_current_page_with_no_searches(self):
        factories.TermFactory()
        response = self.client.get(self.url)

        html_text = '<a class="page-link" href="#">1</a>'
        self.assertContains(response, html_text, html=True)

    def test_dont_have_link_current_page_with_no_items(self):
        factories.TermFactory()
        url = "{}?{}".format(self.url, http.urlencode({"v": "zñ"}))
        response = self.client.get(url)

        html_text = '<a class="page-link" href="#">1</a>'
        self.assertNotContains(response, html_text, html=True)

    def test_has_link_current_page(self):
        term = factories.TermFactory()
        searched_value = term.value[:2]
        url = "{}?{}".format(self.url, http.urlencode({"v": searched_value}))
        response = self.client.get(url)

        html_text = '<a class="page-link" href="#">1</a>'
        self.assertContains(response, html_text, html=True)

    def test_has_link_to_next_page(self):
        num_items_per_page = views.TermSearchView.paginate_by

        for n in range(num_items_per_page + 1):
            term = factories.TermFactory(value="a" * (n + 1))
            factories.DefinitionFactory(term=term)

        url = "{}?{}".format(self.url, http.urlencode({"v": "a"}))
        response = self.client.get(url)

        self.assertContains(
            response,
            '<a class="page-link" href="?page=2">2</a>',
            html=True,
        )
        self.assertContains(
            response,
            '<a class="page-link" href="?page=2">Siguiente &#8594;</a>',
            html=True,
        )

    def test_has_link_to_first_page(self):
        num_items_per_page = views.IndexView.paginate_by

        for n in range(num_items_per_page + 1):
            term = factories.TermFactory(value="a" * (n + 1))
            factories.DefinitionFactory(term=term)

        url = "{}?{}".format(self.url, http.urlencode({"v": "a", "page": 2}))
        response = self.client.get(url)

        response = self.client.get(url)

        self.assertContains(
            response,
            '<a class="page-link" href="?page=1">1</a>',
            html=True,
        )
        self.assertContains(
            response,
            '<a class="page-link" href="?page=1">&#8592; Anterior</a>',
            html=True,
        )
