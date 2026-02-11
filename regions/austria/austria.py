from regions.region import Region
from pandas import json_normalize

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
        }).set_index("id")

        locations['lat'], locations['lon'] = locations['lat'].astype(
            'float'), locations['lon'].astype('float')
        
        self._processLocationList(locations)
        self._processIndividualLocations(locations)
        return locations


