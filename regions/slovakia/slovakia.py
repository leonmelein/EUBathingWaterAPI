from regions.region import Region


class Slovakia(Region):
    url = 'https://geoserver.isuvz.uvzsr.sk/geoserver/wfs'
    
    def __init__(self):
        Region.__init__(self, 'sk', 'Slovakia')

    def ingest(self):
        data = self.loadWFSLayer('hzp:gis_v_r_mapa_ek_sk', self.url)
        data['lat'], data['lon'] = data['geometry'].y, data['geometry'].x
        data.rename(mapper={
            'Názov': 'name'
        }, axis=1, inplace=True)
        data['alternate_name'] = data['name']
        data = data[[
            'id', 'name', 'alternate_name', 'lat', 'lon'
        ]]
        data['country'] = self.iso_code
        
        self._processLocationList(data)
        self._processIndividualLocations(data)
        return data
