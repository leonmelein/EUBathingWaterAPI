from pandas import json_normalize

from regions.region import Region


class Austria(Region):
    url = 'https://www.ages.at/typo3temp/badegewaesser_db.json'

    def __init__(self):
        Region.__init__(self, "at", "Austria")

    def ingest(self):
        data = self.loadJSON(self.url)

        # Unpack from Bundeslander level to national level
        dataset = []
        for item in data["BUNDESLAENDER"]: 
            dataset = dataset + item['BADEGEWAESSER']
        df = json_normalize(dataset)
        locations = df[[
            "BADEGEWAESSERID", "BADEGEWAESSERNAME", "BEZIRK", "LATITUDE", "LONGITUDE"
        ]].rename(columns={
            "BADEGEWAESSERID": "id",
            "BADEGEWAESSERNAME": "name",
            "BEZIRK": "alternate_name",
            "LATITUDE": "lat",
            "LONGITUDE": "lon"
        })

        locations['lat'], locations['lon'] = locations['lat'].astype(
            'float'), locations['lon'].astype('float')
        locations['country'] = self.iso_code
        
        self._processLocationList(locations)
        self._processIndividualLocations(locations)
        return locations


