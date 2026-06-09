from datetime import UTC, datetime
from faker import Faker
from xkcdpass import xkcd_password
from .db import Star


def get_now():
	now = datetime.now(UTC)
	return now

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
