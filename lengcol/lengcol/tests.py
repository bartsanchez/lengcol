import io

from django import test
from django.core import management
from django.urls import reverse


class UnmigratedApplicationsTests(test.TestCase):
    def test_all_apps_migrated(self):
        f = io.StringIO()
        management.call_command("makemigrations", dry_run=True, stderr=f, stdout=f)
        self.assertEqual(f.getvalue(), "No changes detected\n")


class RobotsTxtTests(test.TestCase):
    def test_robots_txt_content(self):
        response = self.client.get(reverse("robots-txt"))

        content = (
            "User-agent: *\n"
            "Allow: /\n\n"
            "Sitemap: https://www.lenguajecoloquial.com/sitemap.xml"
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, content)
