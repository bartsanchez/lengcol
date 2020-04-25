from unittest import mock

import pytest
import requests

W3_VALIDATOR_URL = 'https://validator.w3.org/nu/'


class W3ValidatorMixin:
    @mock.patch('django.middleware.csrf.get_token', return_value='fake_csrf')
    @pytest.mark.vcr(match_on=['body', 'method', 'uri'])
    def test_is_w3_valid(self, csrf_mock):
        index_web = self.client.get(self.url)

        request = requests.post(
            W3_VALIDATOR_URL,
            headers={'Content-Type': 'text/html', 'charset': 'utf-8'},
            params={'out': 'json'},
            data=index_web.getvalue()
        )

        self.assertEqual(request.status_code, 200)
        self.assertListEqual(request.json()['messages'], [])
