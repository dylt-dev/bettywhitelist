import sqlite3
import unittest
from content.code import db

class DbTests(unittest.TestCase):
	def test_connect(self):
		(conn, cur) = db.connect()
		self.assertIsNotNone(conn)
		self.assertIsNotNone(cur)

	# Not a test
	def add_star(self):
		print()
		(conn, cur) = db.connect()
		self.assertIsNotNone(conn)
		self.assertIsNotNone(cur)
		star = create_star()
		with conn:
			db.add_star(cur, star)
		self.assertEqual(1, cur.rowcount)

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
		print()
		with sqlite3.connect('db/bwl.db') as conn:
			self.assertIsNotNone(conn)
			cur = conn.cursor()
			self.assertIsNotNone(cur)
			sql = "DROP TABLE star"
			cur.execute(sql)

	# Not a test
	def get_star_count(self):
		print()
		(conn, cur) = db.connect()
		self.assertIsNotNone(conn)
		self.assertIsNotNone(cur)
		with conn:
			n = db.get_star_count(cur)
		print(f'{n} row(s)')

	# Not a test
	def list_stars(self):
		print()
		(conn, cur) = db.connect()
		self.assertIsNotNone(conn)
		self.assertIsNotNone(cur)
		with conn:
			rows = db.get_stars(cur)
		for row in rows:
			print(row)
			


def create_star() -> db.Star:
	return db.faker.bwl_star()

