from datetime import datetime
import sys
import db
from db.StarClaim import StarClaim
db_dir = dir(db)
sys_path = sys.path

d = []
(conn, cur) = db.connect()
with conn:
    starClaims = StarClaim.get_all(cur)
for starClaim in starClaims:
    o = {}
    o['idStar'] = starClaim.idStar
    o['idClaim'] = starClaim.idClaim
    o['name'] = starClaim.name
    o['email'] = starClaim.email
    o['token'] = starClaim.token
    o['star_created_on'] = datetime.fromisoformat(starClaim.starCreatedOn)
    o['claim_created_on'] = starClaim.claimCreatedOn
    d.append(o)
