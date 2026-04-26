import pickle

from regions.region import Region


class Cyprus(Region):
    dataPath = "data/EEA_BathingWater_2024.pickle"

    def __init__(self):
        Region.__init__(self, 'cy', 'Cyprus')

    def ingest(self):
        with open(self.dataPath, 'rb') as dataSource:
            df = pickle.load(dataSource)

        cyprus = df.loc[(df["countryCode"] == "CY") & (df["season"] == 2024)]
        cyprus = cyprus[[
            "bathingWaterIdentifier",
            "bathingWaterName",
            "lon",
            "lat"
        ]]
        cyprus.rename({
            "bathingWaterIdentifier": "id",
            "bathingWaterName": "name",
        }, axis=1, inplace=True)
        cyprus['name'] = cyprus['name'].str.title()
        cyprus['country'] = self.iso_code
        
        self._processLocationList(cyprus)
        self._processIndividualLocations(cyprus)
        return cyprus
