from definitions import factories, services
from django import test


class DefinitionGatherinTests(test.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.service = services.DefinitionGathering
        cls.fake_def_1 = factories.DefinitionFactory(value='l')
        cls.fake_def_2 = factories.DefinitionFactory(value='o')
        cls.fake_def_3 = factories.DefinitionFactory(value='e')
        cls.fake_def_4 = factories.DefinitionFactory(value='d', active=False)
        cls.objects = [cls.fake_def_1, cls.fake_def_2, cls.fake_def_3]

    def test_get_definitions(self):
        self.assertListEqual(
            list(self.service._get_definitions()),
            self.objects,
        )

    def test_get_definitions__order__asc(self):
        self.assertListEqual(
            list(self.service._get_definitions(order_by='value')),
            [self.fake_def_3, self.fake_def_1, self.fake_def_2],
        )

    def test_get_definitions__order__desc(self):
        self.assertListEqual(
            list(self.service._get_definitions(order_by='-value')),
            [self.fake_def_2, self.fake_def_1, self.fake_def_3],
        )

    def test_get_definitions__items__less_than_total(self):
        self.assertListEqual(
            list(self.service._get_definitions(items=2)),
            [self.fake_def_1, self.fake_def_2],
        )

    def test_get_definitions__items__equal_than_total(self):
        self.assertListEqual(
            list(self.service._get_definitions(items=3)),
            self.objects,
        )

    def test_get_definitions__items__more_than_total(self):
        self.assertListEqual(
            list(self.service._get_definitions(items=4)),
            self.objects,
        )

    def test_get_last_definitions(self):
        self.assertListEqual(
            list(self.service.get_last_definitions(items=2)),
            [self.fake_def_3, self.fake_def_2],
        )
