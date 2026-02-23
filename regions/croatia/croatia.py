from regions.region import Region

import pandas as pd

class Croatia(Region):
    url = "https://vrtlac.izor.hr/ords/kakvoca/kakvoce_sve_json?p_jezik=en"

    def __init__(self):
        Region.__init__(self, "hr", "Croatia")

    def ingest(self):
        data = self.loadJSON(self.url)
        df = pd.json_normalize(data['markers'])
        df = df[[
            'lat', 'lng', 'lsta', 'lpla'
        ]]
        df.rename(mapper={
            "lsta": "id",
            "lpla": "name",
            "lng": "lon"
        }, axis=1, inplace=True)
        df = df[[
            "id", "name", "lat", "lon"
        ]]

        self._processLocationList(df)
        self._processIndividualLocations(df)
        return df