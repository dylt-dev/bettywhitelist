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

	@classmethod
	def from_row(cls, row):
		(name, token, created_on) = row
		star = Star(name=name, token=token, createdOn=created_on)
		return star


@dataclass
class StarClaim:
	idStar: int
	idClaim: int
	name: str
	token: str
	email: str
	starCreatedOn: datetime
	claimCreatedOn: datetime

	@classmethod
	def from_row(cls, row):
		(idStar, idClaim, name, token, email, star_created_on, claim_created_on) = row
		starClaim = StarClaim(idStar=idStar, idClaim=idClaim, name=name, token=token, email=email, starCreatedOn=star_created_on, claimCreatedOn=claim_created_on)
		return starClaim
		


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

def connect():
	conn = sqlite3.connect('/Users/chris/src/bettywhitelist/db/bwl.db')
	if not conn:
		return (None, None)
	cur = conn.cursor()
	return (conn, cur)


def get_now():
	now = datetime.now(UTC)
	return now


def get_star(cur, idStar):
		sql = "SELECT name, token, created_on FROM `star` WHERE id=:idStar"
		params = {"idStar": idStar}
		cur.execute(sql, params)
		row = cur.fetchone()
		if not row:
			return None
		star = Star.from_row(row)
		return star


def get_star_count(cur):
	sql = "SELECT COUNT(*) FROM `star`"
	cur.execute(sql)
	row = cur.fetchone()
	n = row[0]
	return n


def get_star_claim(cur, idStar):
	sql = '''
	SELECT id_star, id_claim, name, token, email, star_created_on, claim_created_on
	FROM `v_star_claim`
	WHERE id_star=:idStar
	'''
	params = {"idStar": idStar}
	cur.execute(sql, params)
	row = cur.fetchone()
	if not row:
		return None
	starClaim = StarClaim.from_row(row)
	return starClaim


def get_star_claims(cur):
	data = []
	sql = 'SELECT id_star, id_claim, name, token, email, star_created_on, claim_created_on from v_star_claim'
	cur.execute(sql)
	while True:
		row = cur.fetchone()
		if not row:
			break
		starClaim = StarClaim.from_row(row)
		data.append(starClaim)
	return data	


def get_stars(cur):
	data = []
	sql = 'SELECT name, token, created_on from star'
	cur.execute(sql)
	while True:
		row = cur.fetchone()
		if not row:
			break
		star = Star.from_row(row)
		data.append(star)
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


def create_token():
	token = faker.xkcd_password()
	return token


faker = create_faker()
# Add method for xkcd password
# import & try from REPL
# make a unit test
# Create a faker for star rows
# make a unit test
# Integrate into unit tests