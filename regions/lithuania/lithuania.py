from regions.region import Region

class Lithuania(Region):
    url = "https://www.inspire-geoportal.lt/geoserver/ows"

    def __init__(self):
        Region.__init__(self, 'lt', 'Lithuania')

    def ingest(self):
        data = self.loadWFSLayer('pds_22_01:AM.BathingWaters', self.url)
        data['name'] = data['name'].apply(lambda x: x.title())
        data['lat'], data['lon'] = [item.y for item in data['geometry']], [item.x for item in data['geometry']]
        data = data[['localid', 'name', 'lat', 'lon']]

        self._processLocationList(data)
        self._processIndividualLocations(data)
        return data