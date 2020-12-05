import re
from unittest import mock

import pytest
import requests

W3_VALIDATOR_URL = 'https://validator.w3.org/nu/'


class W3ValidatorMixin:
    @mock.patch('django.middleware.csrf.get_token', return_value='fake_csrf')
    @pytest.mark.vcr(match_on=['body', 'method', 'uri'])
    def test_is_w3_valid(self, csrf_mock):
        if hasattr(self, 'user'):
            self.client.login(username=self.user, password='fake_password')

        index_web = self.client.get(self.url)

        request = requests.post(
            W3_VALIDATOR_URL,
            headers={'Content-Type': 'text/html', 'charset': 'utf-8'},
            params={'out': 'json'},
            data=index_web.getvalue()
        )

        self.assertEqual(request.status_code, 200)
        self.assertListEqual(request.json()['messages'], [])


class HTMLValidatorMixin:
    def test_has_correct_h1_header(self):
        if hasattr(self, 'user'):
            self.client.login(username=self.user, password='fake_password')

        html_content = self.client.get(self.url).content

        h1_header_re = re.compile(b'<h1>(.*)</h1>')

        result = re.findall(h1_header_re, html_content)

        self.assertEqual(len(result), 1)

        h1_header = result[0].decode()

        self.assertEqual(h1_header, self.h1_header)
