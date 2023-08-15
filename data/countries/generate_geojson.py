from geojson import Feature, Point, FeatureCollection, dump
import sqlite3

db = sqlite3.connect("data/countries/dataset.sqlite3")

cur = db.cursor()
results = cur.execute("SELECT * FROM locations").fetchall()

collection = []
for result in results:
    feature = Feature(id=result[0],
                      geometry=Point((result[4], result[3])),
                      properties={
        "name": result[1],
        "alternate_name": result[2]
    })
    collection.append(feature)

data = FeatureCollection(collection)
with open("locs.geojson", "w") as f:
    dump(data, f)