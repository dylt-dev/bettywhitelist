from datetime import datetime
import dbznutz 

raise Exception("oopsie")

d = []
(conn, cur) = dbznutz.connect()
with conn:
    starClaims = dbznutz.get_star_claims(cur)
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
