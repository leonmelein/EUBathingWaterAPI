from regions.region import Region
from pandas import json_normalize, Series
import numpy as np

class Sweden(Region):
    url = "https://badplatsen.havochvatten.se/badplatsen/api/feature/"

    def __init__(self):
        Region.__init__(self, 'se', 'Sweden')

    def ingest(self):
        data = self.loadJSON(self.url)
        df = json_normalize(data['features'])

        df = df[["properties.NUTSKOD", "properties.NAMN", "properties.KMN_NAMN", "geometry.coordinates"]]
        df[['lat', 'lon']] = df['geometry.coordinates'].apply(
            lambda c: Series(self._split_coords(c))
        )
        df.drop('geometry.coordinates', axis=1, inplace=True)
        df = df.rename(columns={
            "properties.NUTSKOD": 'id', 
            "properties.NAMN": 'name', 
            "properties.KMN_NAMN": 'alternate_name', 
            "geometry.coordinates": 'geometry'
        })

        self._processLocationList(df)
        self._processIndividualLocations(df)

        return df

    def _split_coords(self, coords):
        if isinstance(coords, (list, tuple)) and len(coords) >= 2:
            return coords[0], coords[1]
        return np.nan, np.nan  # or (None, None)
