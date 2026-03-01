from regions.region import Region

class Finland(Region):
    url = "https://paikkatiedot.ymparisto.fi/geoserver/inspire_am2/wfs"

    def __init__(self):
        Region.__init__(self, 'fi', 'Finland')

    def ingest(self):
        dataset = self.loadWFSLayer('inspire_am2:AM.BathingWaters', self.url)
        data = dataset[[
            "uimavesitunnus",
            "uimavesinimi",
            "koorderlong",
            "koorderlat"
        ]]
        data.rename(mapper={
                "uimavesitunnus": "id",
                "uimavesinimi": "name",
                "koorderlong": "lon",
                "koorderlat": "lat"
        }, axis=1, inplace=True)

        self._processLocationList(data)
        self._processIndividualLocations(data)
        return data