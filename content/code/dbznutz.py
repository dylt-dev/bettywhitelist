import sqlite3
from dataclasses import dataclass
from datetime import datetime, UTC
from faker import Faker
from faker.providers import BaseProvider
from xkcdpass import xkcd_password

@dataclass
class Star:
	name: str
	token: str
	createdOn: datetime


def add_star(cur, star: Star):
	sql = """
	INSERT into star
		(name, token, created_on)
		VALUES
		(:name, :token, :created_on)
	"""
	params = {"name": star.name, "token": star.token, "created_on": star.createdOn.isoformat()}
	cur.execute(sql, params)
	row = cur.fetchone()


def connect():
	conn = sqlite3.connect('/Users/chris/src/bettywhitelist/db/bwl.db')
	if not conn:
		return (None, None)
	cur = conn.cursor()
	return (conn, cur)


def get_now():
	now = datetime.now(UTC)
	return now


def get_star_count(cur):
	sql = "SELECT COUNT(*) FROM `star`"
	cur.execute(sql)
	row = cur.fetchone()
	n = row[0]
	return n


def get_stars(cur):
	data = []
	sql = 'SELECT name, token, created_on from star'
	cur.execute(sql)
	while True:
		row = cur.fetchone()
		if not row:
			break
		(name, token, created_on) = row
		data.append(Star(name=name, token=token, createdOn=created_on))
	return data	
# Create faker baseclass
class XkcdPasswordProvider:
	def xkcd_password(self):
		wordlist = xkcd_password.generate_wordlist()
		s=xkcd_password.generate_xkcdpassword(wordlist, numwords=4, delimiter='-')
		return s


class StarProvider:
	def bwl_star(self):
		name = faker.name()
		token = faker.xkcd_password()
		createdOn = faker.date_this_year()
		star = Star(name=name, token=token, createdOn=createdOn)
		return star


def create_faker():
	faker = Faker()
	faker.add_provider(XkcdPasswordProvider())
	faker.add_provider(StarProvider())
	return faker

faker = create_faker()
# Add method for xkcd password
# import & try from REPL
# make a unit test
# Create a faker for star rows
# make a unit test
# Integrate into unit tests