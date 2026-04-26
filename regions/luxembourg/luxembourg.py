from pandas import Series, json_normalize

from regions.region import Region


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

        data['alternate_name'] = data['name']
        data[['lon', 'lat']] = data['coordinates'].apply(Series)
        data = data.reindex(columns=["id", "name", "alternate_name", "lat", "lon"])
        locations = data.sort_values(by="name")
        locations['country'] = self.iso_code
        
        self._processLocationList(locations)
        self._processIndividualLocations(locations)

        return locations