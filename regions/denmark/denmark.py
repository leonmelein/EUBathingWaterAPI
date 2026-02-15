from regions.region import Region
from pandas import DataFrame

class Denmark(Region):
    url = 'https://pulsgeo.miljoeportal.dk/geoserver/wfs'

    def __init__(self):
        Region.__init__(self, 'dk', 'Denmark')

    def ingest(self):
        data = self.loadWFSLayer('puls:Badevand', self.url)
        data = data[data["Closed"].isna()] # Remove all closed sights
        data = data[["Dkbw", "Name", "geometry"]] # Limit columns

        # Split geometry into lat lon
        data['lon'] = data['geometry'].x
        data['lat'] = data['geometry'].y
        data.drop(labels=['geometry'], axis=1, inplace=True)
        data.rename(mapper={
            "Dkbw": "id",
            "Name": "name"
        }, axis=1, inplace=True)
        df = DataFrame(data)

        self._processLocationList(df)
        self._processIndividualLocations(df)
        return data
