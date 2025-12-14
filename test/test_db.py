import sqlite3
import unittest
from content.code import dbznutz

class DbTests(unittest.TestCase):
	def test_connect(self):
		(conn, cur) = dbznutz.connect()
		self.assertIsNotNone(conn)
		self.assertIsNotNone(cur)

	# Not a test
	def add_star(self):
		(conn, cur) = connect()
		star = create_star(self)
		with conn:
			dbznutz.add_star(cur, star)
		self.assertEqual(1, cur.rowcount)

	# Not a test
	def create_claim_table(self):
		(conn, cur) = connect(self)
		with conn:
			sql = """
			CREATE TABLE claim (
				id INTEGER PRIMARY KEY,
				id_star INTEGER,
				email varchar(200),
				created_on DATETIME DEFAULT CURRENT_TIMESTAMP
			)
			"""
			cur.execute(sql)

	def create_claim_table_new(self):
		(conn, cur) = connect(self)
		with conn:
			drop_table(self, cur, 'claim')
			sql = """
			CREATE TABLE claim_new (
				id INTEGER PRIMARY KEY,
				id_star INTEGER,
				email varchar(200),
				created_on DATETIME DEFAULT CURRENT_TIMESTAMP,
				FOREIGN KEY(id_star) REFERENCES star(id)
			)
			"""
			cur.execute(sql)

	# Not a test
	def create_star_table(self):
		(conn, cur) = connect(self)
		with conn:
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
	def create_star_table_new(self):
		(conn, cur) = connect(self)
		with conn:
			sql = """
			CREATE TABLE IF NOT EXISTS star_new (
				id INTEGER PRIMARY KEY,
				name varchar(200) unique,
				token varchar(200),
				created_on DATETIME DEFAULT CURRENT_TIMESTAMP
			)
			"""
			cur.execute(sql)

	def drop_claim_table(self):
		(conn, cur) = connect(self)
		with conn:
			drop_table(self, cur, "claim")

	# Not a test
	def drop_star_table(self):
		(conn, cur) = connect(self)
		with conn:
			drop_table(self, cur, "star")

	# Not a test
	def get_star_count(self):
		print()
		(conn, cur) = connect()
		with conn:
			n = dbznutz.get_star_count(cur)
		print(f'{n} row(s)')

	# Not a test
	def list_star_claims(self):
		print()
		(conn, cur) = connect(self)
		with conn:
			rows = dbznutz.get_star_claims(cur)
		for row in rows:
			print(row)

	# Not a test
	def list_stars(self):
		print()
		(conn, cur) = connect()
		with conn:
			rows = dbznutz.get_stars(cur)
		for row in rows:
			print(row)
			


def connect(t):
	(conn, cur) = dbznutz.connect()
	t.assertIsNotNone(conn)
	t.assertIsNotNone(cur)
	return (conn, cur)


def create_star(t) -> dbznutz.Star:
	return dbznutz.faker.bwl_star()


def drop_table(t, cur, tableName):
	sql = f"DROP TABLE IF EXISTS `{tableName}`"
	cur.execute(sql)
