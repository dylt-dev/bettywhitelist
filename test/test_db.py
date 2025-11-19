import sqlite3
import unittest

class DbTests(unittest.TestCase):
    def test_connect(self):
        with sqlite3.connect('db/bwl.db') as conn:
            self.assertIsNotNone(conn)

    # Not a test
    def add_star(self):
        with sqlite3.connect('db/bwl.db') as conn:
            self.assertIsNotNone(conn)
            cur = conn.cursor()
            self.assertIsNotNone(cur)
            sql = """
            INSERT into star
                (name, token)
                VALUES
                (:name, :token)
            """
            params = {"name": "me", "token": "a-b-c-d"}
            cur.execute(sql, params)

    # Not a test
    def create_table(self):
        with sqlite3.connect('db/bwl.db') as conn:
            self.assertIsNotNone(conn)
            cur = conn.cursor()
            self.assertIsNotNone(cur)
            sql = """
            CREATE TABLE star (
                id INTEGER PRIMARY KEY,
                name varchar(200),
                token varchar(200),
                created_on DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
            cur.execute(sql)

    # Not a test
    def drop_table(self):
        with sqlite3.connect('db/bwl.db') as conn:
            self.assertIsNotNone(conn)
            cur = conn.cursor()
            self.assertIsNotNone(cur)
            sql = "DROP TABLE star"
            cur.execute(sql)

    # Not a test
    def list_table(self):
        with sqlite3.connect('db/bwl.db') as conn:
            conn = sqlite3.connect('db/bwl.db')
            self.assertIsNotNone(conn)
            cur = conn.cursor()
            self.assertIsNotNone(cur)
            sql = 'SELECT name, token from star'
            cur.execute(sql)
            while True:
                row = cur.fetchone()
                if not row:
                    break
                print(row)
                


def add_star(cur, name, token):
    pass

def list_stars(cur):
    pass