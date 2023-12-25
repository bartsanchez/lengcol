import freezegun
from authentication import factories as auth_factories
from base import mixins
from django import test

from definitions import factories


@freezegun.freeze_time("2020-01-01")
class OtherDefinitionDetailViewTests(
    test.TestCase,
    mixins.W3ValidatorMixin,
    mixins.HTMLValidatorMixin,
    mixins.MetaDescriptionValidatorMixin,
):
    page_title = "Lenguaje Coloquial | Definiciones de popular term por fake_username"
    h1_header = "Definición de popular term"
    meta_description = "popular term se define en español como fake definition."

    @classmethod
    def setUpTestData(cls):
        cls.client = test.Client()
        cls.user = auth_factories.UserFactory()
        cls.term = factories.TermFactory(value="popular term")
        cls.definition = factories.DefinitionFactory(
            uuid="6b4a7a9f-3b8f-494b-8565-f960065802ba",
            term=cls.term,
            value="fake definition",
            user=cls.user,
        )
        cls.url = cls.definition.get_absolute_url()

        factories.DefinitionFactory(
            uuid="d4c9aa71-ff3e-4dd3-9bec-8c64b0f9ab6b",
            term=cls.term,
            value="another definition",
        )
        factories.DefinitionFactory(
            uuid="24b77ed6-90b0-47f7-a487-2d09f11ffa23",
            term=cls.term,
            value="one more def",
        )
