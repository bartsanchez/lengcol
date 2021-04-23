from unittest import mock

from django import test
from django.db.models import signals

from authentication import models as auth_models
from authentication import signals as auth_signals
from definitions import factories


@mock.patch('django.contrib.sitemaps.ping_google')
class PingGoogleForSitemapTests(test.TestCase):
    def setUp(self):
        signals.post_save.disconnect(auth_signals.new_registered_user_handler,
                                     sender=auth_models.User)

    def test_ping_google_for_sitemap__prod(self, ping_google_mock):
        django_settings = {'DJANGO_SETTINGS_MODULE': 'fake-prod'}
        with mock.patch.dict('os.environ', django_settings):
            factories.DefinitionFactory()
            ping_google_mock.assert_called_once_with(
                sitemap_url='/sitemap.xml'
            )

    def test_ping_google_for_sitemap__not_prod(self, ping_google_mock):
        factories.DefinitionFactory()
        ping_google_mock.assert_not_called()
