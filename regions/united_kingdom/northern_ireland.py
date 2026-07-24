import pandas as pd

from regions.region import Region


class NorthernIreland(Region):
    url = "https://services-eu1.arcgis.com/kswen6BYexuc1SUk/arcgis/rest/services/BathingWatersDirectiveProtectedAreas/FeatureServer/0/query?where=1%3D1&outFields=Name,PA_CD,centroidX,centroidY&returnGeometry=false&outSR=4326&f=json"


    def __init__(self):
        Region.__init__(self, 'uk', 'United Kingdom', 'Northern Ireland')
    
    def ingest(self):
        data = self.loadJSON(self.url)
        df = pd.json_normalize(data['features'])
        df = df.rename(columns={
            "attributes.PA_CD": "id",
            "attributes.Name": "name",
            "attributes.centroidX": "lon",
            "attributes.centroidY": "lat"
        })
        df['name'].str.title()
        df['country'] = self.iso_code
        return df[[
            'id', 'name', 'country', 'lon', 'lat'
        ]]
