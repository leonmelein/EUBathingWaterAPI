from regions.region import Region
import pandas as pd
import pickle


class Spain(Region):
    dataPath = "data/EEA_BathingWater_2024.pickle"

    def __init__(self):
        Region.__init__(self, 'es', 'Spain')

    def ingest(self):
        with open(self.dataPath, 'rb') as dataSource:
            df = pickle.load(dataSource)

        spain = df.loc[(df["countryCode"] == "ES") & (df["season"] == 2024)]
        spain = spain[[
            "bathingWaterIdentifier",
            "bathingWaterName",
            "lon",
            "lat"
        ]]
        spain.rename({
            "bathingWaterIdentifier": "id",
            "bathingWaterName": "name",
        }, axis=1, inplace=True)
        spain['name'] = spain['name'].str.title()
        
        self._processLocationList(spain)
        self._processIndividualLocations(spain)
        return spain

