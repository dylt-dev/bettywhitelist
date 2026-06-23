import os
from . import db

starClaim = None
db_path = os.getenv("DB_PATH")
if not db_path:
    raise Exception("DB_PATH not set")
(conn, cur) = db.connect(db_path)
claimCode = http.args['claimCode'].strip() # pyright: ignore[reportUndefinedVariable]
with conn:
    starClaims = db.StarClaim.get_by_claim_code(cur, claimCode)
if not starClaims:
    http.redirect('/claimCode-noRows') # pyright: ignore[reportUndefinedVariable]
elif len(starClaims) > 1:
    raise(f'Multiple stars found for claim code "{claimCode}"')
else:
    starClaim = starClaims[0]
    if starClaim.isClaimed:
        http.redirect('/claimCode-isClaimed') # pyright: ignore[reportUndefinedVariable]
# All is well - on to the template!