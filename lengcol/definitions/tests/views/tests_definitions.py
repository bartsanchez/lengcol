import freezegun
import pytest
from django import test
from django.urls import reverse

from authentication import factories as auth_factories
from base import mixins
from definitions import factories, models


class DefinitionCreateViewTests(test.TestCase, mixins.W3ValidatorMixin):
    def setUp(self):
        self.client = test.Client()
        self.user = auth_factories.UserFactory()
        self.url = reverse('definition-add')
        self.management_data = {
            "example_set-TOTAL_FORMS": "2",
            "example_set-INITIAL_FORMS": "0",
            "example_set-MIN_NUM_FORMS": "0",
            "example_set-MAX_NUM_FORMS": "5",
            "example_set-0-value": "",
            "example_set-0-id": "",
            "example_set-0-definition": "",
            "example_set-1-value": "",
            "example_set-1-id": "",
            "example_set-1-definition": ""
        }

    def _login(self):
        self.client.login(username=self.user.username,
                          password='fake_password')

    def test_template_extends(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'lengcol/base.html')

    def test_redirects(self):
        self.assertEqual(models.Definition.objects.count(), 0)

        form_data = {'term': 'fake term', 'value': 'fake definition'}
        form_data.update(self.management_data)

        response = self.client.post(self.url, form_data)

        definition = models.Definition.objects.get()

        self.assertRedirects(response, definition.get_absolute_url())

    def test_add_new(self):
        self.assertEqual(models.Term.objects.count(), 0)
        self.assertEqual(models.Definition.objects.count(), 0)

        self._login()

        form_data = {'term': 'fake term', 'value': 'fake definition'}
        form_data.update(self.management_data)

        response = self.client.post(self.url, form_data, follow=True)

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

        form_data = {
            'term': 'fake term',
            'value': 'fake definition',
        }
        form_data.update(self.management_data)
        form_data['example_set-0-value'] = 'fake example'

        response = self.client.post(self.url, form_data, follow=True,)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(models.Term.objects.count(), 1)
        self.assertEqual(models.Definition.all_objects.count(), 1)
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

        form_data = {'term': 'fake term', 'value': 'fake definition'}
        form_data.update(self.management_data)

        response = self.client.post(self.url, form_data, follow=True)

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

        form_data = {'value': 'fake definition'}
        form_data.update(self.management_data)

        response = self.client.post(self.url, form_data, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(models.Term.objects.count(), 0)
        self.assertEqual(models.Definition.objects.count(), 0)

    def test_missing_value(self):
        self.assertEqual(models.Term.objects.count(), 0)
        self.assertEqual(models.Definition.objects.count(), 0)

        form_data = {'term': 'fake term'}
        form_data.update(self.management_data)

        response = self.client.post(self.url, form_data, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(models.Term.objects.count(), 1)
        self.assertEqual(models.Definition.objects.count(), 0)

        self.assertEqual(
            models.Term.objects.first().value,
            'fake term',
        )

    def test_set_logged_in_user(self):
        self._login()

        form_data = {'term': 'fake term', 'value': 'fake definition'}
        form_data.update(self.management_data)

        response = self.client.post(self.url, form_data, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(models.Definition.objects.count(), 1)

        self.assertEqual(
            models.Definition.objects.first().user,
            self.user,
        )

    def test_dont_set_not_logged_in_user(self):
        form_data = {'term': 'fake term', 'value': 'fake definition'}
        form_data.update(self.management_data)

        response = self.client.post(self.url, form_data, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(models.Definition.objects.count(), 1)

        self.assertIsNone(models.Definition.objects.first().user)

    def test_has_author(self):
        self._login()

        form_data = {'term': 'fake term', 'value': 'fake definition'}
        form_data.update(self.management_data)

        response = self.client.post(self.url, form_data, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Autor: {}'.format(self.user.username))

    def test_has_no_author(self):
        form_data = {'term': 'fake term', 'value': 'fake definition'}
        form_data.update(self.management_data)

        response = self.client.post(self.url, form_data, follow=True)

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

    def test_has_link_to_term_detail(self):
        response = self.client.get(self.url)

        self.assertContains(
            response,
            f'<a href="{self.term.get_absolute_url()}">fake term</a>',
            html=True
        )

    def test_has_link_to_definition_update(self):
        self.client.login(username=self.user.username,
                          password='fake_password')
        response = self.client.get(self.url)

        self.assertContains(
            response,
            '<a href="{}">&#9998; Editar</a>'.format(
                reverse('definition-update',
                        kwargs={'uuid': self.definition.uuid})
            ),
            html=True
        )

    def test_hasnt_link_to_definition_update__another_user(self):
        another_user = auth_factories.UserFactory(
            username='another_username',
        )
        self.client.login(username=another_user,
                          password='fake_password')
        response = self.client.get(self.url)

        self.assertNotContains(
            response,
            '<a href="{}">&#9998; Editar</a>'.format(
                reverse('definition-update',
                        kwargs={'uuid': self.definition.uuid})
            ),
            html=True
        )

    def test_hasnt_link_to_definition_update__anonymous(self):
        response = self.client.get(self.url)

        self.assertNotContains(
            response,
            '<a href="{}">&#9998; Editar</a>'.format(
                reverse('definition-update',
                        kwargs={'uuid': self.definition.uuid})
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


class DefinitionUpdateViewTests(test.TestCase, mixins.W3ValidatorMixin):
    def setUp(self):
        self.client = test.Client()
        self.user = auth_factories.UserFactory()
        self.definition = factories.DefinitionFactory(
            uuid='869fc83b-2004-428d-9870-9089a8f29f20',
            user=self.user,
        )
        self.url = reverse(
            'definition-update',
            kwargs={'uuid': self.definition.uuid}
        )
        self.management_data = {
            "example_set-TOTAL_FORMS": "2",
            "example_set-INITIAL_FORMS": "0",
            "example_set-MIN_NUM_FORMS": "0",
            "example_set-MAX_NUM_FORMS": "5",
            "example_set-0-value": "",
            "example_set-0-id": "",
            "example_set-0-definition": "",
            "example_set-1-value": "",
            "example_set-1-id": "",
            "example_set-1-definition": ""
        }

    def _login(self):
        self.client.login(username=self.user.username,
                          password='fake_password')

    def test_update_definition(self):
        self.assertEqual(models.Term.objects.count(), 1)
        self.assertEqual(models.Definition.objects.count(), 1)
        self.assertEqual(
            self.definition.uuid,
            '869fc83b-2004-428d-9870-9089a8f29f20',
        )
        self.assertEqual(self.definition.term.value, 'term fake')
        self.assertEqual(self.definition.value, 'definition fake')
        self.assertEqual(self.definition.user, self.user)

        self._login()

        form_data = {
            'term': self.definition.term.value,
            'value': 'updated fake definition',
        }
        form_data.update(self.management_data)

        response = self.client.post(self.url, form_data, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(models.Term.objects.count(), 1)
        self.assertEqual(models.Definition.objects.count(), 1)

        self.assertEqual(
            models.Term.objects.first().value,
            'term fake',
        )
        self.assertEqual(
            models.Definition.objects.first().value,
            'updated fake definition',
        )

    def test_update_definition__not_owner(self):
        self.assertEqual(models.Term.objects.count(), 1)
        self.assertEqual(models.Definition.objects.count(), 1)
        self.assertEqual(
            self.definition.uuid,
            '869fc83b-2004-428d-9870-9089a8f29f20',
        )
        self.assertEqual(self.definition.term.value, 'term fake')
        self.assertEqual(self.definition.value, 'definition fake')
        self.assertEqual(self.definition.user, self.user)

        another_user = auth_factories.UserFactory(
            username='another_username',
        )
        self.assertNotEqual(self.user, another_user)

        self.client.login(username=another_user.username,
                          password='fake_password')

        form_data = {
            'term': self.definition.term.value,
            'value': 'updated fake definition',
        }
        form_data.update(self.management_data)

        response = self.client.post(self.url, form_data, follow=True)

        self.assertEqual(response.status_code, 403)

        self.assertEqual(models.Term.objects.count(), 1)
        self.assertEqual(models.Definition.objects.count(), 1)

        self.assertEqual(
            models.Term.objects.first().value,
            'term fake',
        )
        self.assertEqual(
            models.Definition.objects.first().value,
            'definition fake',
        )

    def test_update_definition__not_authenticated(self):
        self.assertEqual(models.Term.objects.count(), 1)
        self.assertEqual(models.Definition.objects.count(), 1)
        self.assertEqual(
            self.definition.uuid,
            '869fc83b-2004-428d-9870-9089a8f29f20',
        )
        self.assertEqual(self.definition.term.value, 'term fake')
        self.assertEqual(self.definition.value, 'definition fake')
        self.assertEqual(self.definition.user, self.user)

        form_data = {
            'term': self.definition.term.value,
            'value': 'updated fake definition',
        }
        form_data.update(self.management_data)

        response = self.client.post(self.url, form_data, follow=True)

        self.assertEqual(response.status_code, 404)

        self.assertEqual(models.Term.objects.count(), 1)
        self.assertEqual(models.Definition.objects.count(), 1)

        self.assertEqual(
            models.Term.objects.first().value,
            'term fake',
        )
        self.assertEqual(
            models.Definition.objects.first().value,
            'definition fake',
        )

    def test_update_definition__get(self):
        self._login()

        response = self.client.get(self.url, follow=True)

        self.assertEqual(response.status_code, 200)

    def test_update_definition__get__not_owner(self):
        another_user = auth_factories.UserFactory(
            username='another_username',
        )
        self.assertNotEqual(self.user, another_user)

        self.client.login(username=another_user.username,
                          password='fake_password')

        response = self.client.get(self.url, follow=True)

        self.assertEqual(response.status_code, 403)

    def test_update_definition__get__not_authenticated(self):
        response = self.client.get(self.url, follow=True)

        self.assertEqual(response.status_code, 404)

    def test_update_definition__remove_example(self):
        self.assertEqual(models.Definition.objects.count(), 1)

        foo_example = factories.ExampleFactory(
            value="foo", definition=self.definition
        )
        bar_example = factories.ExampleFactory(
            value="bar", definition=self.definition
        )

        self.assertEqual(models.Example.objects.count(), 2)
        self.assertEqual(models.Example.all_objects.count(), 2)

        self._login()

        form_data = {
            'term': self.definition.term.value,
            'value': 'updated fake definition',
        }
        management_data = {
            "example_set-TOTAL_FORMS": "4",
            "example_set-INITIAL_FORMS": "2",
            "example_set-MIN_NUM_FORMS": "0",
            "example_set-MAX_NUM_FORMS": "5",
            "example_set-0-value": "foo",
            "example_set-0-id": "{}".format(foo_example.pk),
            "example_set-0-definition": "{}".format(self.definition.pk),
            "example_set-0-DELETE": "on",
            "example_set-1-value": "bar",
            "example_set-1-id": "{}".format(bar_example.pk),
            "example_set-1-definition": "{}".format(self.definition.pk),
            "example_set-2-value": "",
            "example_set-2-id": "",
            "example_set-2-definition": "{}".format(self.definition.pk),
            "example_set-3-value": "",
            "example_set-3-id": "",
            "example_set-3-definition": "{}".format(self.definition.pk),
        }
        form_data.update(management_data)

        response = self.client.post(self.url, form_data, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(models.Definition.objects.count(), 1)
        self.assertEqual(models.Example.objects.count(), 1)
        self.assertEqual(models.Example.all_objects.count(), 2)

        example = models.Example.objects.first()

        self.assertEqual(example.value, 'bar')
        self.assertEqual(example.definition, self.definition)

    def test_update_definition__change_term(self):
        self.assertEqual(models.Term.objects.count(), 1)
        self.assertEqual(models.Definition.objects.count(), 1)
        self.assertEqual(
            self.definition.uuid,
            '869fc83b-2004-428d-9870-9089a8f29f20',
        )
        self.assertEqual(self.definition.term.value, 'term fake')
        self.assertEqual(self.definition.value, 'definition fake')
        self.assertEqual(self.definition.user, self.user)

        self._login()

        form_data = {
            'term': 'updated term fake',
            'value': 'updated fake definition',
        }
        form_data.update(self.management_data)

        response = self.client.post(self.url, form_data, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(models.Term.objects.count(), 2)
        self.assertEqual(models.Definition.objects.count(), 1)

        first_term = models.Term.objects.get(value='term fake')
        second_term = models.Term.objects.get(value='updated term fake')

        self.assertEqual(first_term.definitions.count(), 0)
        self.assertEqual(second_term.definitions.count(), 1)
        self.assertEqual(second_term.definitions.first(), self.definition)

    # TODO: check weird behaviour
    def test_update_definition__missing_value(self):
        self.assertEqual(models.Term.objects.count(), 1)
        self.assertEqual(models.Definition.objects.count(), 1)
        self.assertEqual(
            self.definition.uuid,
            '869fc83b-2004-428d-9870-9089a8f29f20',
        )
        self.assertEqual(self.definition.term.value, 'term fake')
        self.assertEqual(self.definition.value, 'definition fake')
        self.assertEqual(self.definition.user, self.user)

        self._login()

        form_data = {'term': 'updated term fake'}
        form_data.update(self.management_data)

        response = self.client.post(self.url, form_data, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(models.Term.objects.count(), 2)
        self.assertEqual(models.Definition.objects.count(), 1)

        first_term = models.Term.objects.get(value='term fake')
        second_term = models.Term.objects.get(value='updated term fake')

        self.assertEqual(first_term.definitions.count(), 1)
        self.assertEqual(first_term.definitions.first(), self.definition)
        self.assertEqual(second_term.definitions.count(), 0)

    def test_update_definition__change_term_multiple_defs(self):
        other_def = factories.DefinitionFactory(term=self.definition.term)

        self.assertEqual(models.Term.objects.count(), 1)
        self.assertEqual(models.Definition.objects.count(), 2)
        self.assertEqual(
            self.definition.uuid,
            '869fc83b-2004-428d-9870-9089a8f29f20',
        )
        self.assertEqual(self.definition.term.value, 'term fake')
        self.assertEqual(self.definition.value, 'definition fake')
        self.assertEqual(self.definition.user, self.user)

        self._login()

        form_data = {
            'term': 'updated term fake',
            'value': 'updated fake definition',
        }
        form_data.update(self.management_data)

        response = self.client.post(self.url, form_data, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(models.Term.objects.count(), 2)
        self.assertEqual(models.Definition.objects.count(), 2)

        first_term = models.Term.objects.get(value='term fake')
        second_term = models.Term.objects.get(value='updated term fake')

        self.assertEqual(first_term.definitions.count(), 1)
        self.assertEqual(first_term.definitions.first(), other_def)
        self.assertEqual(second_term.definitions.count(), 1)
        self.assertEqual(second_term.definitions.first(), self.definition)


class DefinitionDisableViewTests(test.TestCase, mixins.W3ValidatorMixin):
    def setUp(self):
        self.client = test.Client()
        self.user = auth_factories.UserFactory()
        self.definition = factories.DefinitionFactory(
            uuid='869fc83b-2004-428d-9870-9089a8f29f20',
            user=self.user,
        )
        self.url = reverse(
            'definition-disable',
            kwargs={'uuid': self.definition.uuid}
        )

    def _login(self):
        self.client.login(username=self.user.username,
                          password='fake_password')

    def test_confirm_message_appear_in_view(self):
        term_text = self.definition.term.value

        self._login()

        response = self.client.get(self.url)

        self.assertContains(
            response,
            'Se va a proceder a eliminar la definición '
            f'"{term_text}". ¿Estás seguro?'
        )

    def test_confirm_message_appear_in_view__another_user(self):
        another_user = auth_factories.UserFactory(
            username='another_username',
        )
        self.client.login(username=another_user,
                          password='fake_password')

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_disable_definition(self):
        self.assertEqual(models.Term.objects.count(), 1)
        self.assertEqual(models.Definition.objects.count(), 1)
        self.assertEqual(
            self.definition.uuid,
            '869fc83b-2004-428d-9870-9089a8f29f20',
        )
        self.assertEqual(self.definition.term.value, 'term fake')
        self.assertEqual(self.definition.value, 'definition fake')
        self.assertEqual(self.definition.user, self.user)

        self.assertTrue(models.Term.objects.first().active)
        self.assertTrue(models.Definition.objects.first().active)

        self._login()

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)

        self.assertEqual(models.Term.objects.count(), 1)
        self.assertEqual(models.Definition.objects.count(), 0)
        self.assertEqual(models.Definition.all_objects.count(), 1)

        self.assertTrue(models.Term.objects.first().active)
        self.assertFalse(models.Definition.all_objects.first().active)

    def test_disable_definition__another_user(self):
        self.assertEqual(models.Definition.objects.count(), 1)

        another_user = auth_factories.UserFactory(
            username='another_username',
        )
        self.client.login(username=another_user,
                          password='fake_password')

        self.assertTrue(models.Term.objects.first().active)
        self.assertTrue(models.Definition.objects.first().active)

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 404)

        self.assertEqual(models.Definition.objects.count(), 1)
        self.assertTrue(models.Definition.objects.first().active)
