import requests
import pandas as pd
import sqlite3

from shapely.geometry import Point
from geopandas import GeoDataFrame

from regions.region import Region

class Ireland(Region):
    url = "https://data.epa.ie/bw/api/v1/locations?per_page=500"

    def __init__(self):
        Region.__init__(self, "ie", "Ireland")

    def ingest(self):
        rawData = self.loadJSON(self.url)
        df = pd.json_normalize(rawData['list'])
        geometry = [Point(x, y) for x, y in zip(df['easting'], df['northing'])]
        gdf = GeoDataFrame(df, geometry=geometry)
        gdf.set_crs(29903, inplace=True)
        print(gdf.crs)
        gdf = gdf.to_crs(4326)
        print(gdf.crs)

        lat, lon = [item.y for item in gdf['geometry']], [item.x for item in gdf['geometry']]
        gdf['lat'] = lat
        gdf['lon'] = lon
        gdf = gdf.drop(columns=['easting', 'northing', 'geometry'])
        gdf.rename(mapper={
            "beach_id": "id",
            "beach_name": "name"
        }, axis=1, inplace=True)
        gdf = gdf[[
            "id", "name", "lat", "lon"
        ]]

        self._processLocationList(gdf)
        self._processIndividualLocations(gdf)
        return gdf



