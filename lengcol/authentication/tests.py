from django import test
from django.contrib import auth
from django.urls import reverse
from django.utils import http

import splinter

from base import mixins

from authentication import factories


class LoginViewTests(test.TestCase, mixins.W3ValidatorMixin):
    def setUp(self):
        self.url = reverse('login')
        self.user = factories.UserFactory()

    def fill_and_send_form(self, browser, username, password):
        browser.fill('username', username)
        browser.fill('password', password)
        browser.find_by_id('login-form').click()

    def test_login_view(self):
        with splinter.Browser('django') as browser:
            browser.visit(self.url)

            self.assertIn('Usuario: Anónimo', browser.html)

            self.fill_and_send_form(browser, 'fake_username', 'fake_password')

            self.assertIn('Usuario: fake_user', browser.html)

            self.assertEqual(browser.url, reverse('index'))

    def test_login_view__with_next(self):
        search_url = reverse('term-search')
        url = '{}?{}'.format(self.url,
                             http.urlencode({'next': search_url}))
        with splinter.Browser('django') as browser:
            browser.visit(url)

            self.assertIn('Usuario: Anónimo', browser.html)

            self.fill_and_send_form(browser, 'fake_username', 'fake_password')

            self.assertIn('Usuario: fake_user', browser.html)

            self.assertEqual(browser.url, search_url)

    def test_login_view__failing(self):
        with splinter.Browser('django') as browser:
            browser.visit(self.url)

            self.assertIn('Usuario: Anónimo', browser.html)

            self.fill_and_send_form(browser, 'fake_username', 'wrong_password')

            self.assertIn('Usuario: Anónimo', browser.html)

            self.assertEqual(browser.url, self.url)


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


class RegisterViewTests(test.TestCase, mixins.W3ValidatorMixin):
    def setUp(self):
        self.url = reverse('register')

    def fill_and_send_form(self, browser, username, password1, password2,
                           email):
        browser.fill('username', username)
        browser.fill('password1', password1)
        browser.fill('password2', password2)
        browser.fill('email', email)
        browser.find_by_id('register-form').click()

    def test_register_view(self):
        with splinter.Browser('django') as browser:
            browser.visit(self.url)

            self.assertEqual(auth.get_user_model().objects.count(), 0)

            self.fill_and_send_form(
                browser=browser,
                username='fake_user',
                password1='fake_password',
                password2='fake_password',
                email='foo@bar.qux',
            )

            self.assertEqual(auth.get_user_model().objects.count(), 1)

            user = auth.get_user_model().objects.first()
            self.assertEqual(user.username, 'fake_user')
            self.assertEqual(user.email, 'foo@bar.qux')
            self.assertFalse(user.is_staff)
            self.assertFalse(user.is_superuser)

            self.assertEqual(browser.url, reverse('index'))

    def test_register_existing_user(self):
        self.user = factories.UserFactory(username='fake_user')

        with splinter.Browser('django') as browser:
            browser.visit(self.url)

            self.assertEqual(auth.get_user_model().objects.count(), 1)

            self.fill_and_send_form(
                browser=browser,
                username='fake_user',
                password1='fake_password',
                password2='fake_password',
                email='foo@bar.qux',
            )

            self.assertEqual(auth.get_user_model().objects.count(), 1)

            self.assertIn(
                'A user with that username already exists.',
                browser.html
            )

            self.assertEqual(browser.url, self.url)
