import sqlite3


db = sqlite3.connect("dataset.sqlite3")

dbContext = db.cursor()
#dbContext.execute("CREATE TABLE locations(id, name, alternate_name, lat, long)")
dbContext.execute("CREATE TABLE status(id, status, temperature, timestamp)")

dbContext.execute("""CREATE TABLE locations(
 'id', 'name', 'alternate_name', 'placename', 'current_status', 'description', 'photos', 'website', 'lat', 'lon', 'eu_designation', 'e_coli', 'int_ent', 'amenities', 'warnings'
)""")
dbContext.close()
