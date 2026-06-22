import os
os.environ["SPLUNGE_CODEFOLDER"] = "./mycode"
os.environ["SPLUNGE_TEMPLATE_FOLDER"] = "./mycode"

import os
import sqlite3
import unittest
import werkzeug
from splunge import app


_BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_DB_DIR = os.path.join(_BASEDIR, 'db')
_DB_PATH = os.path.join(_DB_DIR, 'bwl.db')

_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS "star" (
    id INTEGER PRIMARY KEY,
    name varchar(200) unique,
    token varchar(200),
    created_on DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "claim" (
    id INTEGER PRIMARY KEY,
    id_star INTEGER,
    email varchar(200),
    created_on DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(id_star) REFERENCES star(id)
);
CREATE VIEW IF NOT EXISTS v_star_claim AS
SELECT star.id AS id_star, claim.id AS id_claim, star.name,
       star.token, claim.email, star.created_on AS star_created_on,
       claim.created_on AS claim_created_on
FROM star LEFT JOIN claim ON claim.id_star = star.id;
"""

_SEED_SQL = """
INSERT OR IGNORE INTO star (id, name, token, created_on)
VALUES (1, 'Test Star', 'bazooka-override-apostle-suction', datetime('now'));
"""


class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.chdir('./content')
        cls._init_db()

    @classmethod
    def _init_db(cls):
        os.makedirs(_DB_DIR, exist_ok=True)
        conn = sqlite3.connect(_DB_PATH)
        cur = conn.cursor()
        cur.executescript(_SCHEMA_SQL)
        cur.executescript(_SEED_SQL)
        conn.commit()
        conn.close()

    @classmethod
    def tearDownClass(cls):
        os.remove(_DB_PATH)

    def test_list(self):
        test_get(self, "/list", contentType="text/html; charset=utf-8")

    def test_thankyou(self):
        test_get(self, "/thankyou?name=fakename&token=faketoken", contentType="text/html; charset=utf-8")

    def test_index_html(self):
        test_get(self, "/index.html", contentType="text/html")

    def test_nowwhat_md(self):
        test_get(self, "/now-what.md", contentType="text/html; charset=utf-8")

    def test_star(self):
        test_get(self, "/star?id=1", contentType="text/html; charset=utf-8")

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