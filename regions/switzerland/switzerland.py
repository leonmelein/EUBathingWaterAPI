import pandas as pd

from regions.region import Region


class Switzerland(Region):
    url = "https://api3.geo.admin.ch/rest/services/api/MapServer/find?layer=ch.bafu.gewaesserschutz-badewasserqualitaet&sr=4326&geometryFormat=geojson&searchText=CH&searchField=id"

    def __init__(self):
        Region.__init__(self, "ch", "Switzerland")

    def ingest(self):
        data = self.loadJSON(self.url)
        df = pd.json_normalize(data['results'])\
            .rename(columns={
                'properties.bwname': 'name',
                'properties.label': 'alternate_name'
            })\
            .drop(
                columns=[
                    'type', 'featureId', 'bbox', 'layerBodId', 'layerName',
                    'geometry.type', 'properties.groupid', 'properties.nwunitname', 'properties.gemeinde', 'properties.bwatercat',
                    'properties.canton', 'properties.url', 'properties.baquaimg', 'properties.year_bw', 'properties.qualitaet'
                ]
            )
        
        # Split coordinates into columns
        df[['lon', 'lat']] = df['geometry.coordinates'].apply(pd.Series)
        df['country'] = self.iso_code
        locations = df.drop(columns=['geometry.coordinates'])

        self._processLocationList(locations)
        self._processIndividualLocations(locations)
        return locations
