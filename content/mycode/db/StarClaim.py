from dataclasses import dataclass
from datetime import datetime
from . import get_rows

@dataclass
class StarClaim:
	idStar: int
	idClaim: int
	name: str
	token: str
	email: str
	starCreatedOn: datetime
	claimCreatedOn: datetime

	COL_LIST = '"id_star", "id_claim", "name", "token", "email", "star_created_on", "claim_created_on"'
	TABLE_NAME = '"v_star_claim"'
	@property
	def isClaimed (self): return not not self.claimCreatedOn

	@classmethod
	def from_row(cls, row) -> "StarClaim":
		(idStar, idClaim, name, token, email, star_created_on, claim_created_on) = row
		starClaim = StarClaim(idStar=idStar, idClaim=idClaim, name=name, token=token, email=email, starCreatedOn=star_created_on, claimCreatedOn=claim_created_on)
		return starClaim
	
	@classmethod
	def get_all(cls, cur):
		sql = f'SELECT {cls.COL_LIST} FROM {cls.TABLE_NAME}'
		data = get_rows(cur, cls, sql)	
		return data	

	@classmethod
	def get_by_claim_code(cls, cur, claimCode) -> list["StarClaim"]:
		from . import get_rows
		sql = f'SELECT {cls.COL_LIST} FROM {cls.TABLE_NAME} WHERE token=:claimCode' 
		params = { 'claimCode': claimCode }
		data = get_rows(cur, cls, sql, params)
		return data

	@classmethod
	def get_by_star(cls, cur, idStar) -> list["StarClaim"]:
		from . import get_rows
		sql = f'SELECT {cls.COL_LIST} FROM {cls.TABLE_NAME} WHERE id_star=:idStar'
		params = {"idStar": idStar}
		data = get_rows(cur, cls, sql, params)
		return data


