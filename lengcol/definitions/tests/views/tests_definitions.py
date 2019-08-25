from django import test
from django.core import mail
from django.urls import reverse

from base import mixins

from authentication import factories as auth_factories

from definitions import factories
from definitions import models


class DefinitionCreateViewTests(test.TestCase, mixins.W3ValidatorMixin):
    def setUp(self):
        self.client = test.Client()
        self.url = reverse('definition-add')

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

        self.assertRedirects(
            response,
            reverse('definition-detail', kwargs={'uuid': definition.uuid})
        )

    def test_add_new(self):
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

    def test_dont_set_not_logged_in_user(self):
        response = self.client.post(
            self.url,
            {'term': 'fake term', 'value': 'fake definition'},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(models.Definition.objects.count(), 1)

        self.assertIsNone(models.Definition.objects.first().user)

    def test_set_logged_in_user(self):
        user = auth_factories.UserFactory()

        self.client.login(username=user.username, password='fake_password')

        response = self.client.post(
            self.url,
            {'term': 'fake term', 'value': 'fake definition'},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(models.Definition.objects.count(), 1)

        self.assertEqual(
            models.Definition.objects.first().user,
            user,
        )

    def test_new_definition_send_an_email(self):
        self.assertEqual(len(mail.outbox), 0)

        response = self.client.post(
            self.url,
            {'term': 'fake term', 'value': 'fake definition'},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(mail.outbox), 1)

        email_sent = mail.outbox[0]
        self.assertEqual(email_sent.subject, 'New definition was created')
        self.assertEqual(email_sent.body, 'PK: 1')
        self.assertEqual(email_sent.from_email, 'info@lenguajecoloquial.com')
        self.assertTrue(len(email_sent.to), 1)
        self.assertEqual(email_sent.to[0], 'info@lenguajecoloquial.com')

    def test_has_author(self):
        user = auth_factories.UserFactory()

        self.client.login(username=user.username, password='fake_password')

        response = self.client.post(
            self.url,
            {'term': 'fake term', 'value': 'fake definition'},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Autor: {}'.format(user.username))

    def test_hasnt_author(self):
        response = self.client.post(
            self.url,
            {'term': 'fake term', 'value': 'fake definition'},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Autor: Anónimo')


class DefinitionDetailViewTests(test.TestCase, mixins.W3ValidatorMixin):
    def setUp(self):
        self.client = test.Client()
        self.user = auth_factories.UserFactory()
        self.term = factories.TermFactory(value='fake term')
        self.definition = factories.DefinitionFactory(term=self.term,
                                                      value='fake definition',
                                                      user=self.user)
        self.url = reverse('definition-detail',
                           kwargs={'uuid': self.definition.uuid})

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
        url = reverse('definition-detail',
                      kwargs={'uuid': definition.uuid})

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
        url = reverse('definition-detail',
                      kwargs={'uuid': definition.uuid})

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
            '<a href="{}">fake term</a>'.format(
                reverse('term-detail',
                        kwargs={'slug': self.definition.term.slug})
            ),
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
