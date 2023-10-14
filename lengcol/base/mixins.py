import re
from unittest import mock

import pytest
import requests

W3_VALIDATOR_URL = 'https://validator.w3.org/nu/'


class W3ValidatorMixin:
    @mock.patch(
        'django.template.context_processors.get_token',
        return_value="fake_csrf"
    )
    @pytest.mark.vcr(
        match_on=['body', 'method', 'uri'],
        filter_headers=["CF-RAY", "Date", "Set-Cookie", "x-request-id"]
    )
    def test_is_w3_valid(self, csrf_mock):
        if hasattr(self, 'user'):
            self.client.login(username=self.user, password='fake_password')

        index_web = self.client.get(self.url)

        request = requests.post(
            W3_VALIDATOR_URL,
            headers={'Content-Type': 'text/html', 'charset': 'utf-8'},
            params={'out': 'json'},
            data=index_web.getvalue(),
            timeout=5,
        )

        self.assertEqual(request.status_code, 200)
        self.assertListEqual(request.json()['messages'], [])


class HTMLValidatorMixin:
    def test_has_correct_page_title(self):
        if hasattr(self, 'user'):
            self.client.login(username=self.user, password='fake_password')

        html_content = self.client.get(self.url).content

        page_title_re = re.compile(b'<title>(.*)</title>')

        result = re.findall(page_title_re, html_content)

        self.assertEqual(len(result), 1)

        page_title = result[0].decode()

        self.assertEqual(page_title, self.page_title)

    def test_has_correct_h1_header(self):
        if hasattr(self, 'user'):
            self.client.login(username=self.user, password='fake_password')

        html_content = self.client.get(self.url).content

        h1_header_re = re.compile(b'<h1>(.*)</h1>')

        result = re.findall(h1_header_re, html_content)

        self.assertEqual(len(result), 1)

        h1_header = result[0].decode()

        self.assertEqual(h1_header, self.h1_header)


class MetaDescriptionValidatorMixin:
    def test_has_correct_meta_description(self):
        if hasattr(self, 'user'):
            self.client.login(username=self.user, password='fake_password')

        html_content = self.client.get(self.url).content

        meta_description_re = re.compile(
            b'<meta name="description" content="(.*)">'
        )

        result = re.findall(meta_description_re, html_content)

        self.assertEqual(len(result), 1)

        meta_description = result[0].decode()

        self.assertEqual(meta_description, self.meta_description)
