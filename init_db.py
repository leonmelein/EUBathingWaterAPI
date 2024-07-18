import sqlite3


db = sqlite3.connect("bathingWater.sqlite3")

dbContext = db.cursor()
# dbContext.execute("CREATE TABLE locations(id, name, alternate_name, description, url, lat, long)")
# dbContext.execute("CREATE TABLE status(id, status, temperature, timestamp)")

dbContext.execute("INSERT INTO locations VALUES (1, 'Sloterplas', 'Sloterpark', 'Zwemplas in Amsterdam Nieuw-West', 'https://amsterdam.nl', 52.3657703, 4.819712)")
dbContext.close()   