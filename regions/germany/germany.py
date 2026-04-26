import pandas as pd

from regions.region import Region


class Germany(Region):
    url = "https://geoportal.bafg.de/arcgis3/rest/services/BfG/Badegew%C3%A4sser/MapServer/0/query?where=1%3D1&outFields=BWID,NAME&outSR=4326&f=pjson"

    def __init__(self):
        Region.__init__(self, 'de', 'Germany')

    def ingest(self):
        data = self.loadJSON(self.url)
        df = pd.json_normalize(data['features'])
        df.rename(mapper={
                'attributes.BWID': 'id',
                'attributes.NAME': 'name',
                'geometry.x': 'lon',
                'geometry.y': 'lat'
        }, axis=1, inplace=True)
        df['name'] = df['name'].str.title()
        df['country'] = self.iso_code

        self._processLocationList(df)
        self._processIndividualLocations(df)
        return df
