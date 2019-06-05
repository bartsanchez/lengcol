from django import test
from django.utils import timezone

import freezegun

from base import models


class BaseModelTests(test.TestCase):
    @freezegun.freeze_time('2000-01-05 10:00:05Z')
    def test_created_field(self):
        fake_instance = models.TestModel()
        fake_instance.save()

        self.assertTrue(hasattr(fake_instance, 'created'))
        self.assertEqual(fake_instance.created, timezone.now())

    @freezegun.freeze_time('2000-01-05 10:00:05Z')
    def test_updated_field(self):
        fake_instance = models.TestModel()
        fake_instance.save()

        self.assertTrue(hasattr(fake_instance, 'updated'))
        self.assertEqual(fake_instance.updated, timezone.now())

        self.assertEqual(fake_instance.created, fake_instance.updated)

        with freezegun.freeze_time('2000-01-05 17:50:15Z'):
            fake_instance.save()

            self.assertNotEqual(fake_instance.created, fake_instance.updated)
            self.assertEqual(fake_instance.updated, timezone.now())
