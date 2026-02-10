from regions.region import Region
import pandas as pd
from shapely.geometry import Point
from geopandas import GeoDataFrame

class Wallonia(Region):
    url = "https://geoservices.wallonie.be/arcgis/rest/services/EAU/BAIGNADE/MapServer/0/query?f=json&outfields=*&where=1%3D1"

    def __init__(self):
        Region.__init__(self, "BE-WAL", "Belgium", "Wallonia")

    def ingest(self):
        data = self.loadJSON(self.url)
        crs = data['spatialReference']['wkid']
        locations = data['features']

        df = pd.json_normalize(locations)
        df = df[[
            'attributes.BWID', 'attributes.NOM', 'attributes.COMMUNE', 'geometry.x', 'geometry.y'
        ]]
        geometry = [Point(x, y)
            for x, y in zip(df['geometry.x'], df['geometry.y'])]
        gdf = GeoDataFrame(df, geometry=geometry).set_crs(crs)
        gdf = gdf.to_crs(4326)
        gdf['lat'], gdf['long'] = [item.y for item in gdf['geometry']], [
            item.x for item in gdf['geometry']]
        gdf = gdf.drop(columns=[
            "geometry.x", "geometry.y", "geometry"
        ]).rename(columns={
            "attributes.BWID": "id",
            "attributes.NOM": "name",
            "attributes.COMMUNE": "alternate_name"
        }).set_index("id")

        return gdf