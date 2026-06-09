from datetime import datetime
import urllib.parse
from . import db

# driver = pyodbc.drivers()[-1]
# host='db.bettywhitelist.com'
# db='bwl'
# username='admin'
# password='cheese-viaduct-batt-sodium'
# connString=f"Driver={{{driver}}}; Server={host}; Database={db}; UID={username}; PWD={password};"
# conn = pyodbc.connect(connString)
# cursor = conn.cursor()
# token=xp.generate_xkcdpassword(xp.generate_wordlist(), numwords=4, delimiter='-')
# sql = f"insert into star (token, name) values ('{token}', '{name}')"
# cursor.execute(sql)
# cursor.commit()
# conn.close()

name = http.args['name'] # type: ignore
token = db.create_token()
createdOn = datetime.now()
star = db.Star(name, token, createdOn)

(conn, cur) = db.connect()
with conn:
    db.add_star(cur, star)

# scheme=http.env['wsgi.url_scheme']
# host=http.env["HTTP_HOST"]
# redirect(f'{scheme}://{host}/thankyou.pyp')
nameParam = urllib.parse.quote_plus(name)
tokenParam = urllib.parse.quote_plus(token)
http.redirect(f'thankyou?name={nameParam}&token={tokenParam}') # pyright: ignore[reportUndefinedVariable]
