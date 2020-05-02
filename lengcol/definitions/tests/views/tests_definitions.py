import freezegun
from django import test
from django.conf import settings
from django.core import mail
from django.urls import reverse

from authentication import factories as auth_factories
from base import mixins
from definitions import factories, models


class DefinitionCreateViewTests(test.TestCase, mixins.W3ValidatorMixin):
    def setUp(self):
        self.client = test.Client()
        self.user = auth_factories.UserFactory()
        self.url = reverse('definition-add')

    def _login(self):
        self.client.login(username=self.user.username,
                          password='fake_password')

    def test_template_extends(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'lengcol/base.html')

    def test_redirects(self):
        self.assertEqual(models.Definition.objects.count(), 0)

        response = self.client.post(
            self.url,
            {'term': 'fake term', 'value': 'fake definition'},
        )

        definition = models.Definition.objects.get()

        self.assertRedirects(response, definition.get_absolute_url())

    def test_add_new(self):
        self.assertEqual(models.Term.objects.count(), 0)
        self.assertEqual(models.Definition.objects.count(), 0)

        self._login()
        response = self.client.post(
            self.url,
            {'term': 'fake term', 'value': 'fake definition'},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(models.Term.objects.count(), 1)
        self.assertEqual(models.Definition.objects.count(), 1)

        self.assertEqual(
            models.Term.objects.first().value,
            'fake term',
        )
        self.assertEqual(
            models.Definition.objects.first().value,
            'fake definition',
        )

    def test_add_new__with_example(self):
        self.assertEqual(models.Term.objects.count(), 0)
        self.assertEqual(models.Definition.objects.count(), 0)
        self.assertEqual(models.Example.objects.count(), 0)

        self._login()
        response = self.client.post(
            self.url,
            {
                'term': 'fake term',
                'value': 'fake definition',
                'example': 'fake example'
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(models.Term.objects.count(), 1)
        self.assertEqual(models.Definition.objects.count(), 1)
        self.assertEqual(models.Example.objects.count(), 1)

        definition = models.Definition.objects.first()
        self.assertEqual(definition.value, 'fake definition')

        example = models.Example.objects.first()
        self.assertEqual(example.value, 'fake example')
        self.assertEqual(example.definition, definition)

    def test_add_new__not_logged_user(self):
        self.assertEqual(models.Term.objects.count(), 0)
        self.assertEqual(models.Definition.objects.count(), 0)

        response = self.client.post(
            self.url,
            {'term': 'fake term', 'value': 'fake definition'},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(models.Term.objects.count(), 1)
        self.assertEqual(models.Definition.objects.count(), 1)

        self.assertEqual(
            models.Term.objects.first().value,
            'fake term',
        )
        self.assertEqual(
            models.Definition.objects.first().value,
            'fake definition',
        )

    def test_missing_term(self):
        self.assertEqual(models.Term.objects.count(), 0)
        self.assertEqual(models.Definition.objects.count(), 0)

        response = self.client.post(
            self.url,
            {'value': 'fake definition'},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(models.Term.objects.count(), 0)
        self.assertEqual(models.Definition.objects.count(), 0)

    def test_missing_value(self):
        self.assertEqual(models.Term.objects.count(), 0)
        self.assertEqual(models.Definition.objects.count(), 0)

        response = self.client.post(
            self.url,
            {'term': 'fake term'},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(models.Term.objects.count(), 1)
        self.assertEqual(models.Definition.objects.count(), 0)

        self.assertEqual(
            models.Term.objects.first().value,
            'fake term',
        )

    def test_set_logged_in_user(self):
        self._login()
        response = self.client.post(
            self.url,
            {'term': 'fake term', 'value': 'fake definition'},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(models.Definition.objects.count(), 1)

        self.assertEqual(
            models.Definition.objects.first().user,
            self.user,
        )

    def test_dont_set_not_logged_in_user(self):
        response = self.client.post(
            self.url,
            {'term': 'fake term', 'value': 'fake definition'},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(models.Definition.objects.count(), 1)

        self.assertIsNone(models.Definition.objects.first().user)

    def test_new_definition_send_an_email(self):
        self.assertEqual(len(mail.outbox), 0)

        response = self.client.post(
            self.url,
            {'term': 'fake term', 'value': 'fake definition'},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(models.Definition.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)

        email_sent = mail.outbox[0]
        self.assertEqual(email_sent.subject, 'New definition was created')
        self.assertEqual(email_sent.from_email, settings.APP_EMAIL)
        self.assertTrue(len(email_sent.to), 1)
        self.assertEqual(email_sent.to[0], settings.APP_EMAIL)

        # Body
        definition = models.Definition.objects.first()
        definition_url = definition.get_absolute_url()
        self.assertEqual(
            email_sent.body,
            f'{settings.BASE_URL}{definition_url}'
        )

    def test_has_author(self):
        self._login()
        response = self.client.post(
            self.url,
            {'term': 'fake term', 'value': 'fake definition'},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Autor: {}'.format(self.user.username))

    def test_has_no_author(self):
        response = self.client.post(
            self.url,
            {'term': 'fake term', 'value': 'fake definition'},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Autor: Anónimo')


@freezegun.freeze_time('2020-01-01')
class DefinitionDetailViewTests(test.TestCase, mixins.W3ValidatorMixin):
    def setUp(self):
        self.client = test.Client()
        self.user = auth_factories.UserFactory()
        self.term = factories.TermFactory(value='fake term')
        self.definition = factories.DefinitionFactory(
            uuid='6b4a7a9f-3b8f-494b-8565-f960065802ba',
            term=self.term,
            value='fake definition',
            user=self.user,
        )
        self.url = self.definition.get_absolute_url()

    def test_template_extends(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'lengcol/base.html')

    def test_term(self):
        response = self.client.get(self.url)

        self.assertContains(response, 'fake term')

    def test_definition(self):
        response = self.client.get(self.url)

        self.assertContains(response, 'fake definition')

    def test_creation_date(self):
        response = self.client.get(self.url)

        created = self.definition.created.strftime('%d-%m-%Y')

        self.assertContains(response, 'Fecha de creación {}'.format(created))

    def test_example_creation__same_user(self):
        self.client.login(username=self.user.username,
                          password='fake_password')
        response = self.client.get(self.url)

        self.assertNotContains(response, 'fake example 1')
        self.assertNotContains(response, 'fake example 2')

        response = self.client.post(
            self.url,
            {'example': 'fake example 1'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(models.Example.objects.count(), 1)

        self.assertContains(response, 'fake example 1')
        self.assertNotContains(response, 'fake example 2')

        response = self.client.post(
            self.url,
            {'example': 'fake example 2'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(models.Example.objects.count(), 2)

        self.assertContains(response, 'fake example 1')
        self.assertContains(response, 'fake example 2')

    def test_example_not_logged_user(self):
        response = self.client.get(self.url)

        self.assertNotContains(response, 'fake example 1')
        self.assertNotContains(response, 'fake example 2')

        response = self.client.post(
            self.url,
            {'example': 'fake example 1'},
            follow=True,
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b'Unauthorized')

        self.assertEqual(models.Example.objects.count(), 0)

    def test_example_different_user(self):
        other_user = auth_factories.UserFactory(username='other_user')
        term = factories.TermFactory(value='other term')
        definition = factories.DefinitionFactory(term=term,
                                                 value='other definition',
                                                 user=other_user)
        url = definition.get_absolute_url()

        self.client.login(username=self.user.username,
                          password='fake_password')
        response = self.client.get(url)

        self.assertNotContains(response, 'fake example 1')
        self.assertNotContains(response, 'fake example 2')

        response = self.client.post(
            url,
            {'example': 'fake example 1'},
            follow=True,
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b'Unauthorized')

        self.assertEqual(models.Example.objects.count(), 0)

    def test_example_does_not_work_for_anonymous_definitions(self):
        term = factories.TermFactory(value='other term')
        definition = factories.DefinitionFactory(term=term,
                                                 value='other definition')
        url = definition.get_absolute_url()

        response = self.client.get(url)

        self.assertNotContains(response, 'fake example 1')
        self.assertNotContains(response, 'fake example 2')

        response = self.client.post(
            url,
            {'example': 'fake example 1'},
            follow=True,
        )
        self.assertEqual(response.status_code, 404)

        self.assertEqual(models.Example.objects.count(), 0)

    def test_has_link_to_term_detail(self):
        response = self.client.get(self.url)

        self.assertContains(
            response,
            f'<a href="{self.term.get_absolute_url()}">fake term</a>',
            html=True
        )

    def test_inactive_examples_does_not_appear(self):
        response = self.client.get(self.url)

        factories.ExampleFactory(definition=self.definition,
                                 value='fake example')

        response = self.client.get(self.url)

        self.assertContains(response, 'fake example')

        self.assertEqual(models.Example.objects.count(), 1)
        example = models.Example.objects.first()

        example.active = False
        example.save()

        response = self.client.get(self.url)

        self.assertNotContains(response, 'fake example')

    def test_invalid_example(self):
        self.client.login(username=self.user.username,
                          password='fake_password')
        response = self.client.get(self.url)

        response = self.client.post(
            self.url,
            {'example': ''},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(models.Example.objects.count(), 0)
