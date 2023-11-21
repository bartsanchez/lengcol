import splinter
from authentication import factories
from base import mixins
from django import test
from django.urls import reverse
from django.utils import http


class LoginViewTests(
    test.TestCase,
    mixins.W3ValidatorMixin,
    mixins.HTMLValidatorMixin,
    mixins.MetaDescriptionValidatorMixin,
):
    page_title = "Lenguaje Coloquial | Diccionario en español"
    h1_header = "Identificación"
    meta_description = (
        "Página de autenticación de usuarios para el proyecto Lenguaje " "Coloquial."
    )

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("login")
        cls.user = factories.UserFactory()

    def fill_and_send_form(self, browser, username, password):
        browser.fill("username", username)
        browser.fill("password", password)
        browser.find_by_id("login-form").click()

    def test_login_view(self):
        with splinter.Browser("django") as browser:
            browser.visit(self.url)

            self.assertIn("Usuario: Anónimo", browser.html)

            self.fill_and_send_form(browser, "fake_username", "fake_password")

            self.assertIn("Usuario: fake_user", browser.html)

            self.assertEqual(browser.url, reverse("index"))

    def test_login_view__with_next(self):
        search_url = reverse("term-search")
        url = "{}?{}".format(self.url, http.urlencode({"next": search_url}))
        with splinter.Browser("django") as browser:
            browser.visit(url)

            self.assertIn("Usuario: Anónimo", browser.html)

            self.fill_and_send_form(browser, "fake_username", "fake_password")

            self.assertIn("Usuario: fake_user", browser.html)

            self.assertEqual(browser.url, search_url)

    def test_login_view__failing(self):
        with splinter.Browser("django") as browser:
            browser.visit(self.url)

            self.assertIn("Usuario: Anónimo", browser.html)

            self.fill_and_send_form(browser, "fake_username", "wrong_password")

            self.assertIn("Usuario: Anónimo", browser.html)

            self.assertEqual(browser.url, self.url)
