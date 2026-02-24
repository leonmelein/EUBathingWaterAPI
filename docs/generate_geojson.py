from geojson import Feature, Point, FeatureCollection, dump

collection = []

for result in results:
    feature = Feature(id=result[0],
                      geometry=Point((result[3], result[4])),
                      properties={
        "name": result[1],
        "alternate_name": result[2]
    })
    collection.append(feature)

data = FeatureCollection(collection)
with open("locations.geojson", "w", encoding="utf8") as f:
    dump(data, f, ensure_ascii=False)

