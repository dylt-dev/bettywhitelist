from datetime import datetime
import dbznutz 

d = []
(conn, cur) = dbznutz.connect()
with conn:
    stars = dbznutz.get_stars(cur)
for star in stars:
    o = {}
    o['name'] = star.name
    # o['created_on'] = datetime.strptime(star.createdOn, "%b %d %Y %-I:%M %p")
    o['created_on'] = datetime.fromisoformat(star.createdOn)
    d.append(o)
