import sqlite3


db = sqlite3.connect("dataset.sqlite3")

dbContext = db.cursor()
dbContext.execute("CREATE TABLE locations(id, name, alternate_name, lat, long)")
dbContext.execute("CREATE TABLE status(id, status, temperature, timestamp)")

