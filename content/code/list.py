import pyodbc
import urllib.parse

driver = pyodbc.drivers()[-1]
host='db.bettywhitelist.com'
db='bwl'
username='admin'
password='cheese-viaduct-batt-sodium'
connString=f"Driver={{{driver}}}; Server={host}; Database={db}; UID={username}; PWD={password};"
conn = pyodbc.connect(connString)
cursor = conn.cursor()
sql = "SELECT name, created_on FROM star ORDER BY created_on"
cursor.execute(sql)
d = []
rs = cursor.fetchall()
for row in rs:
    o = {}
    o['name'] = row.name
    o['created_on'] = row.created_on
    d.append(row)

conn.close()
