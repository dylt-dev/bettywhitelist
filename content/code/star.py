from . import db

idStar = http.args['id'] # pyright: ignore[reportUndefinedVariable]

(conn, cur) = db.connect()
with conn:
    starClaim = db.Star.get()
