import os
from . import db

idStar = http.args['id'] # pyright: ignore[reportUndefinedVariable]

db_path = os.getenv("DB_PATH")
if not db_path:
    raise Exception("DB_PATH not set")
(conn, cur) = db.connect(db_path)
with conn:
    starClaim = db.Star.get(cur, idStar)
