from datetime import datetime
import sys
import db
import os
from db.StarClaim import StarClaim
db_dir = dir(db)
sys_path = sys.path

d = []
db_path = os.getenv("DB_PATH")
if not db_path:
    raise Exception("DB_PATH not set")
(conn, cur) = db.connect(db_path)
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
