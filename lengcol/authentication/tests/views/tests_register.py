from dataclasses import dataclass

import splinter
from base import mixins
from django import test
from django.contrib import auth
from django.urls import reverse

from authentication import factories


@dataclass
class UserInfo:
    username: str
    password1: str
    password2: str
    email: str


class RegisterViewTests(
    test.TestCase,
    mixins.W3ValidatorMixin,
    mixins.HTMLValidatorMixin,
    mixins.MetaDescriptionValidatorMixin,
):
    page_title = "Lenguaje Coloquial | Diccionario en español"
    h1_header = "Crea tu cuenta"
    meta_description = (
        "Página de registro de usuarios para el proyecto Lenguaje Coloquial."
    )

    def setUp(self):
        self.user_info = UserInfo(
            username="fake_user",
            password1="fake_password",
            password2="fake_password",
            email="foo@bar.qux",
        )

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("register")

    def fill_and_send_form(self, browser, user_info: UserInfo):
        browser.fill("username", user_info.username)
        browser.fill("password1", user_info.password1)
        browser.fill("password2", user_info.password2)
        browser.fill("email", user_info.email)
        browser.find_by_id("register-form").click()

    def test_register_view(self):
        with splinter.Browser("django") as browser:
            browser.visit(self.url)

            self.assertEqual(auth.get_user_model().objects.count(), 0)

            self.fill_and_send_form(browser=browser, user_info=self.user_info)

            self.assertEqual(auth.get_user_model().objects.count(), 1)

            user = auth.get_user_model().objects.first()
            self.assertEqual(user.username, "fake_user")
            self.assertEqual(user.email, "foo@bar.qux")
            self.assertFalse(user.is_staff)
            self.assertFalse(user.is_superuser)

            self.assertEqual(browser.url, reverse("index"))

    def test_register_existing_user(self):
        self.user = factories.UserFactory(username="fake_user")

        with splinter.Browser("django") as browser:
            browser.visit(self.url)

            self.assertEqual(auth.get_user_model().objects.count(), 1)

            self.fill_and_send_form(browser=browser, user_info=self.user_info)

            self.assertEqual(auth.get_user_model().objects.count(), 1)

            self.assertIn("A user with that username already exists.", browser.html)

            self.assertEqual(browser.url, self.url)

    def test_user_is_logged_after_register(self):
        with splinter.Browser("django") as browser:
            browser.visit(self.url)

            self.fill_and_send_form(browser=browser, user_info=self.user_info)

            self.assertIn("Usuario: fake_user", browser.html)
