import os
import sqlite3
import tempfile
import unittest
import sys
sys.path.insert(0, 'content/mycode')
from content.mycode import db
from content.mycode.db.Star import Star
from content.mycode.db.StarClaim import StarClaim
from . import util

_DB_DIR = tempfile.TemporaryDirectory("bettywhitelist", "test")
_DB_PATH = os.path.join(_DB_DIR.name, 'bwl.db')

class Tests(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.db_path = util.init_db()

	def test_connect(self):
		(conn, cur) = connect(self)
		self.assertIsNotNone(conn)
		self.assertIsNotNone(cur)

	def test_get_star(self):
		idStar = 6
		(conn, cur) = connect(self)
		with conn:
			star = Star.get(cur, idStar)
			self.assertIsNotNone(star)
			self.assertEqual(idStar, star.id)

	def test_get_star_claims(self):
		(conn, cur) = connect(self)
		with conn:
			rows = StarClaim.get_all(cur)
			nRows = get_row_count(self, cur, 'v_star_claim')
		self.assertIsNotNone(rows)
		self.assertEqual(nRows, len(rows))

	def test_get_star_claims_by_claim_code(self):
		claimCode = "override-apostle-suction-bazooka"
		idStar = 6
		(conn, cur) = connect(self)
		with conn:
			starClaims = StarClaim.get_by_claim_code(cur, claimCode)
		self.assertIsNotNone(starClaims)
		self.assertEqual(1, len(starClaims))
		starClaim = starClaims[0]
		self.assertIsNotNone(starClaim)
		self.assertEqual(idStar, starClaim.idStar)

	def test_get_star_claims_by_star(self):
		idStar = 6
		(conn, cur) = connect(self)
		with conn:
			starClaims = StarClaim.get_by_star(cur, idStar)
		self.assertIsNotNone(starClaims)
		self.assertEqual(1, len(starClaims))
		starClaim = starClaims[0]
		self.assertIsNotNone(starClaim)
		self.assertEqual(idStar, starClaim.idStar)

	def test_get_stars(self):
		(conn, cur) = connect(self)
		with conn:
			rows = Star.get_all(cur)
			nRows = get_row_count(self, cur, 'star')
		self.assertIsNotNone(rows)
		self.assertEqual(nRows, len(rows))

	# Not a test
	def add_star(self):
		(conn, cur) = connect(self)
		with conn:
			rows = Star.get_all(cur)
			nRows = get_row_count(self, cur, 'star')
		self.assertIsNotNone(rows)
		self.assertEqual(nRows, len(rows))

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
		(conn, cur) = connect(self)
		with conn:
			n = Star.get_count(cur)
		print(f'{n} row(s)')

	# Not a test
	def list_star_claims(self):
		print()
		(conn, cur) = connect(self)
		with conn:
			rows = StarClaim.get_all(cur)
		for row in rows:
			print(row)

	# Not a test
	def list_stars(self):
		print()
		(conn, cur) = connect(self)
		with conn:
			rows = Star.get_all(cur)
		for row in rows:
			print(row)
			

def connect(t):
	(conn, cur) = db.connect(t.db_path)
	t.assertIsNotNone(conn)
	t.assertIsNotNone(cur)
	return (conn, cur)


def create_star(t) -> Star:
	return db.faker.bwl_star()


def drop_table(t, cur, tableName):
	sql = f"DROP TABLE IF EXISTS `{tableName}`"
	cur.execute(sql)

def get_row_count(t, cur, tableName):
	sql = f'SELECT COUNT(*) as n from {tableName}'
	cur.execute(sql)
	row = cur.fetchone()
	t.assertIsNotNone(row)
	(nRows, ) = row
	return nRows
