from django import test

from definitions import factories, services


class TermGatherinTests(test.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.service = services.TermGathering
        cls.fake_term_1 = factories.TermFactory(value='l')
        cls.fake_term_2 = factories.TermFactory(value='o')
        cls.fake_term_3 = factories.TermFactory(value='e')
        cls.fake_term_4 = factories.TermFactory(value='d', active=False)
        cls.objects = [cls.fake_term_1, cls.fake_term_2, cls.fake_term_3]

    def test_get_terms(self):
        self.assertListEqual(
            list(self.service._get_terms()),
            self.objects,
        )

    def test_get_terms__order__asc(self):
        self.assertListEqual(
            list(self.service._get_terms(order_by='value')),
            [self.fake_term_3, self.fake_term_1, self.fake_term_2],
        )

    def test_get_terms__order__desc(self):
        self.assertListEqual(
            list(self.service._get_terms(order_by='-value')),
            [self.fake_term_2, self.fake_term_1, self.fake_term_3],
        )

    def test_get_terms__items__less_than_total(self):
        self.assertListEqual(
            list(self.service._get_terms(items=2)),
            [self.fake_term_1, self.fake_term_2],
        )

    def test_get_terms__items__equal_than_total(self):
        self.assertListEqual(
            list(self.service._get_terms(items=3)),
            self.objects,
        )

    def test_get_terms__items__more_than_total(self):
        self.assertListEqual(
            list(self.service._get_terms(items=4)),
            self.objects,
        )

    def test_get_last_terms(self):
        self.assertListEqual(
            list(self.service.get_last_terms(items=2)),
            [self.fake_term_3, self.fake_term_2],
        )
