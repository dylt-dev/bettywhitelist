from datetime import datetime

with open("/tmp/bwl.log", "a") as log:
   import sys
   print(sys.path, file=log)
   print(file=log)
    # print(f'dbznutz.__file__={dbznutz.__file__}', file=log)
    # print(dir(dbznutz), file=log)
   
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
