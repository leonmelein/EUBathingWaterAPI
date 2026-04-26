import pandas as pd

from regions.region import Region


class Slovenia(Region):
    url = "https://gis.arso.gov.si/arcgis/rest/services/Portal/Kopalne_vode_skladnost_MM_2024/MapServer/16/query?where=1%3D1&text=&objectIds=&time=&timeRelation=esriTimeRelationOverlaps&geometry=&geometryType=esriGeometryPoint&inSR=&spatialRel=esriSpatialRelIntersects&distance=&units=esriSRUnit_Foot&relationParam=&outFields=*&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=4326&havingClause=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&historicMoment=&returnDistinctValues=false&resultOffset=&resultRecordCount=&returnExtentOnly=false&sqlFormat=none&datumTransformation=&parameterValues=&rangeValues=&quantizationParameters=&featureEncoding=esriDefault&f=geojson"

    def __init__(self):
        Region.__init__(self, 'si', 'Slovenia')

    def ingest(self):
        data = self.loadJSON(self.url)['features']
        df = pd.json_normalize(data)
        df['lon'] = [item[0] for item in df['geometry.coordinates']]
        df['lat'] = [item[1] for item in df['geometry.coordinates']]
        df = df[[
            'properties.ARSO.KOPALNE_VODE_2024.SIFRA',
            'properties.ARSO.KOPALNE_VODE_2024.OBMOCJE',
            'lon',
            'lat'
        ]]
        df.rename(mapper={
            'properties.ARSO.KOPALNE_VODE_2024.SIFRA': 'id',
            'properties.ARSO.KOPALNE_VODE_2024.OBMOCJE': 'name',
        }, axis=1, inplace=True)
        df['country'] = self.iso_code

        self._processLocationList(df)
        self._processIndividualLocations(df)
        return df