from unittest import mock

import splinter
from django import test
from django.conf import settings
from django.contrib import auth
from django.core import mail
from django.urls import reverse


class NewRegisteredUserMailTests(test.TestCase):
    def setUp(self):
        self.client = test.Client()
        self.url = reverse('register')

    def fill_and_send_form(self, browser, username, password1, password2,
                           email):
        browser.fill('username', username)
        browser.fill('password1', password1)
        browser.fill('password2', password2)
        browser.fill('email', email)
        browser.find_by_id('register-form').click()

    # TODO not sure why this mock is needed but VCR tests fail if not here
    @mock.patch('django.middleware.csrf.get_token', return_value='fake_csrf')
    def test_new_registered_user_send_an_email(self, csrf_mock):
        self.assertEqual(len(mail.outbox), 0)

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
        self.assertEqual(len(mail.outbox), 1)

        email_sent = mail.outbox[0]
        self.assertEqual(email_sent.subject, 'New user was registered')
        self.assertEqual(email_sent.from_email, settings.APP_EMAIL)
        self.assertTrue(len(email_sent.to), 1)
        self.assertEqual(email_sent.to[0], settings.APP_EMAIL)

        # Body
        self.assertEqual(email_sent.body, 'fake_user')
