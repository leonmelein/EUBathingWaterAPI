import pickle

import pandas as pd

from regions.region import Region


class Romania(Region):
    dataPath = "data/EEA_BathingWater_2024.pickle"

    def __init__(self):
        Region.__init__(self, 'ro', 'Romania')

    def ingest(self):
        with open(self.dataPath, 'rb') as dataSource:
            df = pickle.load(dataSource)

        bulgaria = df.loc[(df["countryCode"] == "RO") & (df["season"] == 2024)]
        bulgaria = bulgaria[[
            "bathingWaterIdentifier",
            "bathingWaterName",
            "lon",
            "lat"
        ]]
        bulgaria.rename({
            "bathingWaterIdentifier": "id",
            "bathingWaterName": "name",
        }, axis=1, inplace=True)
        bulgaria['name'] = bulgaria['name'].str.title()
        bulgaria['country'] = self.iso_code
        
        self._processLocationList(bulgaria)
        self._processIndividualLocations(bulgaria)
        return bulgaria

