import dbznutz 

idStar = http.args['id'] # pyright: ignore[reportUndefinedVariable]

(conn, cur) = dbznutz.connect()
with conn:
    starClaim = dbznutz.get_star_claim(cur, idStar)
