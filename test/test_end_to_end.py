import os
import unittest
import werkzeug
from splunge import app


class EndToEndTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.chdir('./content')

    def test_code_list(self):
        test_get(self, "/code/list", contentType="text/html")

    def test_code_thankyou(self):
        test_get(self, "/code/thankyou?name=fakename&token=faketoken", contentType="text/html")

    def test_index_html(self):
        test_get(self, "/index.html", contentType="text/html")

    def test_nowwhat_md(self):
        test_get(self, "/now-what.md", contentType="text/markdown")


def test_get(t: unittest.TestCase, url: str, *, contentType=None):
    cli = werkzeug.Client(app.app)
    resp: werkzeug.Response = cli.get(url)
    statusCode, sep, statusMessage = resp.status.partition(' ')
    t.assertEqual(str(200), statusCode)
    if statusMessage:
        t.assertEqual('OK', statusMessage.upper())
    print(f'resp.text={resp.text}')
    print(f'resp.content_type={resp.content_type}')
    if contentType:
        t.assertEqual(contentType, resp.content_type)  