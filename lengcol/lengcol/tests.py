import io

from django import test
from django.core import management


class UnmigratedApplicationsTests(test.TestCase):
    def test_all_apps_migrated(self):
        f = io.StringIO()
        management.call_command(
            'makemigrations', dry_run=True, stderr=f, stdout=f
        )
        self.assertEqual(f.getvalue(), 'No changes detected\n')
