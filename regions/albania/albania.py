from regions.region import Region
import pickle


class Albania(Region):
    dataPath = "data/EEA_BathingWater_2024.pickle"

    def __init__(self):
        Region.__init__(self, 'al', 'Albania')

    def ingest(self):
        with open(self.dataPath, 'rb') as dataSource:
            df = pickle.load(dataSource)

        albania = df.loc[(df["countryCode"] == "AL") & (df["season"] == 2024)]
        albania = albania[[
            "bathingWaterIdentifier",
            "bathingWaterName",
            "lon",
            "lat"
        ]]
        albania.rename({
            "bathingWaterIdentifier": "id",
            "bathingWaterName": "name",
        }, axis=1, inplace=True)
        albania['name'] = albania['name'].str.title()
        
        self._processLocationList(albania)
        self._processIndividualLocations(albania)
        return albania
