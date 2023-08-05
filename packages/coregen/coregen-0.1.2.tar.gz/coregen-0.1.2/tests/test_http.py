from unittest import TestCase

from coregen.http.url import generate_data_uri


class TestHttp(TestCase):

    def setUp(self):
        self.media = 'test-a/testb-'
        self.base64 = ';base64'
        self.data = 'Adsa!@#4eS1'

    def test_generate_data_uri(self):
        datauri = generate_data_uri(
            mimetype=self.media,
            data=self.data,
            encode_to_b64=True)

        self.assertEqual(
            datauri, 'data:test-a/testb-;base64,QWRzYSFAIzRlUzE=')
