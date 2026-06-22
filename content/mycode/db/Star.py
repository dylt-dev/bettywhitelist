from dataclasses import dataclass
from datetime import datetime
# import __init__

@dataclass
class Star:
	id: int
	name: str
	token: str
	createdOn: datetime

	COL_LIST = '"id", "name", "token", "created_on"'
	TABLE_NAME='"star"'

	@classmethod
	def from_row(cls, row):
		(id, name, token, created_on) = row
		star = Star(id=id, name=name, token=token, createdOn=created_on)
		return star

	@classmethod
	def get(cls, cur, idStar) -> "Star":
		from . import get_object
		star = get_object(cur, cls, idStar)
		return star

	@classmethod
	def get_all(cls, cur) -> list["Star"]:
		from . import get_rows
		sql = f'SELECT {cls.COL_LIST} FROM {cls.TABLE_NAME}'
		data = get_rows(cur, cls, sql)	
		return data	
	
	@classmethod
	def get_count(cls, cur):
		from . import get_row_count
		return get_row_count(cur, cls)


