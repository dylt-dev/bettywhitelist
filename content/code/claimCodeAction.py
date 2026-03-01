from . import db

starClaim = None
(conn, cur) = db.connect()
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