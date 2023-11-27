from authentication import factories as auth_factories
from authentication import models as auth_models
from authentication import signals as auth_signals
from django import test
from django.conf import settings
from django.core import mail
from django.db.models import signals
from django.urls import reverse

from definitions import factories, models


class NewDefinitionMailTests(test.TestCase):
    @classmethod
    def setUpTestData(cls):
        signals.post_save.disconnect(
            auth_signals.new_registered_user_handler,
            sender=auth_models.User,
        )
        cls.client = test.Client()
        cls.user = auth_factories.UserFactory()
        cls.url = reverse("definition-add")
        cls.management_data = {
            "example_set-TOTAL_FORMS": "2",
            "example_set-INITIAL_FORMS": "0",
            "example_set-MIN_NUM_FORMS": "0",
            "example_set-MAX_NUM_FORMS": "5",
            "example_set-0-value": "",
            "example_set-0-id": "",
            "example_set-0-definition": "",
            "example_set-1-value": "",
            "example_set-1-id": "",
            "example_set-1-definition": "",
        }

    def test_new_definition_send_an_email(self):
        self.assertEqual(len(mail.outbox), 0)

        form_data = {"term": "fake term", "value": "fake definition"}
        form_data.update(self.management_data)

        response = self.client.post(self.url, form_data, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(models.Definition.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)

        email_sent = mail.outbox[0]
        self.assertEqual(email_sent.subject, "New definition was created")
        self.assertEqual(email_sent.from_email, settings.APP_EMAIL)
        self.assertTrue(len(email_sent.to), 1)
        self.assertEqual(email_sent.to[0], settings.APP_EMAIL)

        # Body
        definition = models.Definition.objects.first()
        definition_url = definition.get_absolute_url()
        self.assertEqual(email_sent.body, f"{settings.BASE_URL}{definition_url}")

    def test_update_definition_dont_send_an_email(self):
        self.client.login(username=self.user.username, password="fake_password")

        self.assertEqual(len(mail.outbox), 0)

        definition = factories.DefinitionFactory(
            value="fake definition",
            user=self.user,
        )
        self.assertEqual(models.Definition.objects.count(), 1)

        self.assertEqual(len(mail.outbox), 1)

        url = reverse("definition-update", kwargs={"uuid": definition.uuid})

        form_data = {"term": "fake term", "value": "modified definition"}
        form_data.update(self.management_data)

        response = self.client.post(url, form_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Definition.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)
