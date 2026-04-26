import pandas as pd

from regions.region import Region


class Scotland(Region):
    url = "https://map.sepa.org.uk/server/rest/services/Open/Environmental_Monitoring/MapServer/1/query?f=json&where=(1%3D1)%20AND%20(1%3D1)&returnGeometry=true&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=OBJECTID%20ASC&outSR=4326&resultOffset=0&resultRecordCount=100"

    def __init__(self):
        Region.__init__(self, 'uk', 'United Kingdom', 'Scotland')
    
    def ingest(self):
        data = self.loadJSON(self.url)
        df = pd.json_normalize(data['features'])
        df = df.rename(columns={
            "attributes.objectid": "id",
            "attributes.description": "name",
            "geometry.x": "lon",
            "geometry.y": "lat"
        })\
        .drop(columns=[
            'attributes.class_description', 'attributes.bw_url',
            'attributes.year'
        ])
        df['country'] = self.iso_code
        return df
