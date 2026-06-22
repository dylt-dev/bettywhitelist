from datetime import datetime
import os
import sqlite3
import sys
from .Star import Star

_BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
_DB_DIR = os.path.join(_BASEDIR, 'db')

def connect():
	os.makedirs(_DB_DIR, exist_ok=True)
	conn = sqlite3.connect(os.path.join(_DB_DIR, 'bwl.db'))
	if not conn:
		return (None, None)
	cur = conn.cursor()
	return (conn, cur)


def get_object(cur, cls, id):
	sql = f"SELECT {cls.COL_LIST} FROM {cls.TABLE_NAME} WHERE id=:id"
	params = {"id": id}
	cur.execute(sql, params)
	row = cur.fetchone()
	if not row:
		return None
	o = cls.from_row(row)
	return o


def get_row_count(cur, cls):
	sql = f'SELECT COUNT(*) FROM {cls.TABLE_NAME}'
	cur.execute(sql)
	row = cur.fetchone()
	n = row[0]
	return n


def get_rows(cur, cls, sql, params={}):
	data = []
	cur.execute(sql, params)
	while True:
		row = cur.fetchone()
		if not row:
			break
		o = cls.from_row(row)
		data.append(o)
	return data


# def add_star(cur, star: Star):
# 	sql = """
# 	INSERT into star
# 		(name, token, created_on)
# 		VALUES
# 		(:name, :token, :created_on)
# 	"""
# 	params = {"name": star.name, "token": star.token, "created_on": star.createdOn.isoformat()}
# 	cur.execute(sql, params)
# 	row = cur.fetchone()


def claim_star(cur, token, email):
	sql = 'SELECT id FROM star WHERE token=:token'
	params = {"token": token}
	cur.execute(sql, params)
	row = cur.fetchone()
	(idStar,) = row
	print(idStar)
	if idStar:
		createdOn = datetime.now().isoformat()
		params = {"idStar": idStar, "email": email, "createdOn": createdOn}
		sql = """
		INSERT into claim
			(id_star, email, created_on)
		VALUES
		(:idStar, :email, :createdOn)
		"""
		cur.execute(sql, params)
		row = cur.fetchone()
		print(row)
	else:
		print(f"No idStar found for {token}")

