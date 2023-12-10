import splinter
from django import test
from django.urls import reverse

from authentication import factories


class LogoutViewTests(test.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("logout")
        cls.user = factories.UserFactory()

    def fill_and_send_form(self, browser, username, password):
        browser.fill("username", username)
        browser.fill("password", password)
        browser.find_by_id("login-form").click()

    def test_logout_view(self):
        with splinter.Browser("django") as browser:
            browser.visit(reverse("login"))

            self.assertIn("Usuario: Anónimo", browser.html)

            self.fill_and_send_form(browser, "fake_username", "fake_password")

            self.assertIn("Usuario: fake_user", browser.html)

            self.assertEqual(browser.url, reverse("index"))

            browser.find_by_id("logout-button").click()

            self.assertIn("Usuario: Anónimo", browser.html)

    def test_logout_redirect_to_index(self):
        with splinter.Browser("django") as browser:
            browser.visit(reverse("login"))

            self.fill_and_send_form(browser, "fake_username", "fake_password")

            browser.find_by_id("logout-button").click()

            self.assertEqual(browser.url, reverse("index"))

    def test_logout_dont_allow_get_calls(self):
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, 405)

    def test_logout_post_without_login(self):
        with splinter.Browser("django") as browser:
            browser.visit(reverse("login"))
            self.assertIn("Usuario: Anónimo", browser.html)

            request = self.client.post(self.url)
            self.assertEqual(request.status_code, 302)

            self.assertEqual(browser.url, reverse("login"))
            self.assertIn("Usuario: Anónimo", browser.html)
