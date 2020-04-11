import splinter
from django import test
from django.urls import reverse

from authentication import factories


class LogoutViewTests(test.TestCase):
    def setUp(self):
        self.url = reverse('logout')
        self.user = factories.UserFactory()

    def fill_and_send_form(self, browser, username, password):
        browser.fill('username', username)
        browser.fill('password', password)
        browser.find_by_id('login-form').click()

    def test_logout_view(self):
        with splinter.Browser('django') as browser:
            browser.visit(reverse('login'))

            self.assertIn('Usuario: Anónimo', browser.html)

            self.fill_and_send_form(browser, 'fake_username', 'fake_password')

            self.assertIn('Usuario: fake_user', browser.html)

            self.assertEqual(browser.url, reverse('index'))

            browser.visit(self.url)

            self.assertIn('Usuario: Anónimo', browser.html)

    def test_logout_redirect_to_index(self):
        with splinter.Browser('django') as browser:
            browser.visit(reverse('login'))

            browser.visit(self.url)

            self.assertEqual(browser.url, reverse('index'))
