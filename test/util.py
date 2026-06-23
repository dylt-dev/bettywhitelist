import os
import sqlite3
import tempfile
import unittest
from content.mycode import db

_SEED_SQL = """
INSERT OR IGNORE INTO star (id, name, token, created_on)
VALUES (1, 'Test Star', 'bazooka-override-apostle-suction', datetime('now'));

INSERT OR IGNORE INTO star (id, name, token, created_on)
VALUES (6, 'Test Star 6', 'override-apostle-suction-bazooka', datetime('now'));
"""

class Tests(unittest.TestCase):
	# not a test
	def create_app_db(self):
		db_dir = './db'
		db_path = os.path.join(db_dir, 'bwl.db')
		print(db_path)
		conn = sqlite3.connect(db_path)
		cur = conn.cursor()
		cur.executescript(db.SCHEMA)
		conn.commit()
		conn.close()

	

def init_db():
	DB_DIR = tempfile.mkdtemp(prefix="bettywhitelist.", suffix=".test")
	DB_PATH = os.path.join(DB_DIR, 'bwl.db')
	print(DB_PATH)
	os.environ['DB_PATH'] = DB_PATH
	conn = sqlite3.connect(DB_PATH)
	cur = conn.cursor()
	cur.executescript(db.SCHEMA)
	cur.executescript(_SEED_SQL)
	conn.commit()
	conn.close()
	return DB_PATH
