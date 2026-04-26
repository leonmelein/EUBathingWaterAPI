import pandas as pd

from regions.region import Region


class Flanders(Region):
    url = "https://geo.api.vlaanderen.be/VlaamseZwemwaterlocaties/ogc/features/collections/Vlzwl/items?f=application%2Fgeo%2Bjson"

    def __init__(self):
        Region.__init__(self, "BE-VLG", "Belgium", "Flanders")

    def ingest(self):
        data = self.loadJSON(self.url)
        df = pd\
            .json_normalize(data['features'])\
            .drop(columns=['id', 'type', 'geometry_name', 'bbox', 'geometry.type', 'geometry.coordinates', 'properties.OIDN', 'properties.UIDN', 'properties.CYEAR', 'properties.NAMESPACE', 'properties.VERSIONID', 'properties.BEGINLIFE', 'properties.LOCALID', 'properties.ENDLIFE', 'properties.PREDECESID', 'properties.PREDEIDSCH', 'properties.SUCCESSOID', 'properties.SUCCEIDSCH', 'properties.WEVOLUTION', 'properties.NAMETXTLAN', 'properties.DESIGBEGIN', 'properties.DESIGEND', 'properties.ZONETYPE', 'properties.SPZONETYPE', 'properties.RZONEID', 'properties.RZONEIDSCH', 'properties.LEGISNAME', 'properties.LEGISLINK', 'properties.LEGISLEVEL', 'properties.THEMAIDSCH', 'properties.SIZEVALUE', 'properties.SIZEUOM', 'properties.CONFSTATUS', 'properties.LINKKWL', 'properties.STATUSCODE', 'properties.STATUSDATE', 'properties.REMARKS', 'properties.COUNTRY', 'properties.QCCHECK', 'properties.REMARKS2', 'properties.OPMERKINGE'])\
            .rename(columns={'properties.THEMATICID': 'id', 'properties.NAMETEXT': 'name', 'properties.NAMETXTINT': 'alternate_name', 'properties.LON': 'lon', 'properties.LAT': 'lat'})\
            .set_index('id')
        df['alternate_name'] = df['alternate_name'].str.title()
        df['name'] = df['name'].str.title()
        locations = df[['name', 'alternate_name', 'lat', 'lon']]
        locations['country'] = self.iso_code

        return locations