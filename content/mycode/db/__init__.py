from datetime import datetime
import os
import sqlite3
import sys
from .Star import Star

SCHEMA = """
CREATE TABLE IF NOT EXISTS "claim" (
                                id INTEGER PRIMARY KEY,
                                id_star INTEGER,
                                email varchar(200),
                                created_on DATETIME DEFAULT CURRENT_TIMESTAMP,
                                FOREIGN KEY(id_star) REFERENCES star(id)
);
CREATE TABLE IF NOT EXISTS "star" (
                                id INTEGER PRIMARY KEY,
                                name varchar(200) unique,
                                token varchar(200),
                                created_on DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE VIEW v_star_claim as select star.id as id_star, claim.id as id_claim, star.name, star.token, claim.email, star.created_on as star_created_on, claim.created_on as claim_created_on from star left join claim on claim.id_star=star.id
/* v_star_claim(id_star,id_claim,name,token,email,star_created_on,claim_created_on) */;
"""


def connect(path):
	conn = sqlite3.connect(path)
	if not conn:
		raise Exception(f"Unable to connect to database at {path}")
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

