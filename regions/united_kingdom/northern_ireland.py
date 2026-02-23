from regions.region import Region
import pandas as pd

class NorthernIreland(Region):
    url = "https://services-eu1.arcgis.com/kswen6BYexuc1SUk/arcgis/rest/services/BathingWatersDirectiveProtectedAreas/FeatureServer/0/query?where=1%3D1&outFields=Name,PA_CD,centroidX,centroidY&returnGeometry=false&outSR=4326&f=json"


    def __init__(self):
        Region.__init__(self, 'gb-nir', 'United Kingdom', 'Northern Ireland')
    
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
        return df[[
            'id', 'name', 'lon', 'lat'
        ]]
