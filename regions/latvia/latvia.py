import zipfile
from io import BytesIO, StringIO

import kml2geojson
import pandas as pd
import requests

from regions.region import Region


class Latvia(Region):
    url = "https://www.google.com/maps/d/kml?mid=1vP3B4hda5fYtW4GSoQVLJXJxqIM"

    def __init__(self):
        Region.__init__(self, 'lv', 'Latvia')

    def ingest(self):
        data = requests.get(self.url)
        data = BytesIO(data.content)
        zf = zipfile.ZipFile(data, "r")

        kml_name = next((n for n in zf.namelist() if n.lower().endswith(".kml")), None)
        if not kml_name:
            raise FileNotFoundError("No KML file found inside KMZ")

        kml_bytes = zf.read(kml_name)
        kml_text = kml_bytes.decode("utf-8", errors="replace")
        jsondata = kml2geojson.convert(StringIO(kml_text))

        data = pd.json_normalize(jsondata[0]['features'])
        data = data[[
            'properties.name',
            'geometry.coordinates'
        ]]
        data['id'] = self._syntheticIds(len(data))
        data['lon'] = data['geometry.coordinates'].apply(lambda x: x[0])
        data['lat'] = data['geometry.coordinates'].apply(lambda x: x[1])
        data.drop("geometry.coordinates", axis=1, inplace=True)
        data.rename(mapper={
            "properties.name": "name"
        }, axis=1, inplace=True)
        data = data [[
            "id", "name", "lat", "lon"
        ]]
        data['country'] = self.iso_code

        self._processLocationList(data)
        self._processIndividualLocations(data)
        return data

    def _syntheticIds(self, length):
        return [f'{self.iso_code}000{i}' for i in range(1, length + 1)]


