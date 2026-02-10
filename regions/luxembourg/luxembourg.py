from regions.region import Region
from pandas import json_normalize, Series

class Luxembourg(Region):
    url = 'https://data.public.lu/fr/datasets/r/5e3ee76e-f206-4e50-8c4c-4bcffc32f2ed'

    def __init__(self):
        Region.__init__(self, "lu", "Luxembourg")

    def ingest(self):
        data = self.loadJSON(self.url)

        data = json_normalize(data['age_bathing_waters_0']['features'])\
            .rename(columns={
                    "properties.NAME": "name",
                    "geometry.coordinates": "coordinates",
                    "properties.OBJECTID": "id"
            })\
            .set_index("id")

        data['alternate_name'] = data['name']
        data[['long', 'lat']] = data['coordinates'].apply(Series)
        data = data.reindex(columns=["name", "alternate_name", "lat", "long"])
        locations = data.sort_values(by="name")
        
        self._processLocationList(locations)
        self._processIndividualLocations(locations)

        return locations