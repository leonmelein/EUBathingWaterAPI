from io import StringIO

import pandas as pd
import requests
from geopandas import GeoDataFrame
from shapely import Point

from regions.region import Region


class Estonia(Region):
    url = "https://vtiav.sm.ee/index.php/opendata/supluskohad.xml"

    def __init__(self):
        Region.__init__(self, 'ee', 'Estonia - WORK IN PROGRESS')

    def ingest(self):
        data = requests.get(self.url).text

        df = pd.read_xml(
            StringIO(data),
            stylesheet='./regions/estonia/transform.xslt',
            xpath=".//row"
        )
        
        geometry = [Point(y, x) for y, x in zip(df['y'], df['x'])]
        df.drop(labels=['x', 'y'], axis=1, inplace=True)

        gdf = GeoDataFrame(data=df, geometry=geometry)
        gdf.set_crs(3301, inplace=True)

        result = gdf.to_crs(4326)
        result['lon'] = result.geometry.x
        result['lat'] = result.geometry.y
        result = result.dropna(subset=["lon", "lat"])

        output = pd.DataFrame(result[[
            'id', 'name', 'lat', 'lon'
        ]])
        output['country'] = self.iso_code

        self._processLocationList(output)
        self._processIndividualLocations(output)
        return output