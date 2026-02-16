from regions.region import Region
from pandas import json_normalize

class Czechia(Region):
    url = 'https://geoportal.mzcr.cz/server/rest/services/VerejneAplikace/KoupaciVody_View/MapServer/0/query?f=pjson&cacheHint=true&resultOffset=0&resultRecordCount=2000&where=1%3D1&orderByFields=OBJECTID&outFields=*&outSR=4326&spatialRel=esriSpatialRelIntersects'

    def __init__(self):
        Region.__init__(self, 'cz', 'Czechia')

    def ingest(self):
        data = self.loadJSON(self.url)
        json_df = json_normalize(data['features'])
        json_df = json_df[[
            'attributes.id',
            'attributes.title',
            'attributes.type',
            'geometry.y',
            'geometry.x',
        ]]
        json_df.rename(mapper={
            'attributes.id': 'id',
            'attributes.title': 'name',
            'attributes.type': 'alternate_name',
            'geometry.y': 'lat',
            'geometry.x': 'lon'
        }, axis=1, inplace=True)

        self._processLocationList(json_df)
        self._processIndividualLocations(json_df)
        return json_df