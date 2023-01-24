import requests
from dateutil import parser
from Models.ZwemwaterNL.Advice import Advice
from Models.ZwemwaterNL.Tests import Tests

from Models.Area import Area
from Models.WaterQuality import WaterQuality


class ZwemwaterNL:
    server = 'https://pubgeo.zwemwater.nl/geoserver/zwr_public/wfs'
    locations = ["1092", "1093", "1153", "1158",
                "304872", "5934676", "6102791", "7179850"]
                
    def info(self, location="1458"):
        body = f"""
        <GetFeature xmlns="http://www.opengis.net/wfs" service="WFS" version="1.1.0" outputFormat="application/json" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <Query typeName="zwr_public:zwemplekken_details" srsName="EPSG:28992" xmlns:zwr_public="https://pubgeo.zwemwater.nl/geoserver/zwr_public">
                    <Filter xmlns="http://www.opengis.net/ogc">
                        <PropertyIsEqualTo>
                            <PropertyName>zwemwaterlocatie_id</PropertyName>
                            <Literal>{location}</Literal>
                        </PropertyIsEqualTo>
                    </Filter>
                </Query>
            </GetFeature>
        """
        response = requests.post(self.server, body)
        details = response.json()['features'][0]['properties']
        naam, rating = details['naam'], details['status']
        return (naam, rating)

    def retrieve(self, location="1458"):
        name, rating = self.info(location)

        body = f"""
            <GetFeature xmlns="http://www.opengis.net/wfs" service="WFS" version="1.1.0" outputFormat="application/json" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <Query typeName="zwr_public:resultaatsen" srsName="EPSG:28992" xmlns:zwr_public="https://pubgeo.zwemwater.nl/geoserver/zwr_public">
                    <Filter xmlns="http://www.opengis.net/ogc">
                        <PropertyIsEqualTo>
                            <PropertyName>zwemwaterlocatie_id</PropertyName>
                            <Literal>{location}</Literal>
                        </PropertyIsEqualTo>
                    </Filter>
                </Query>
            </GetFeature>
        """

        response = requests.post(self.server, body)
        data = [item['properties'] for item in response.json()['features']]

        status = []
        for item in ["E_COLI", "INTTNLETRCCN"]:
            measurements = [x for x in data if x["type_object_code"] == item]
            sorted_measurements = sorted(measurements, key=lambda x: parser.parse(x['object_begin_tijd']), reverse=True)
            measurement_type, value = sorted_measurements[0]["type_object_code"], sorted_measurements[0][
                "numerieke_waarde"]
            is_safe = self.is_value_safe(measurement_type, value)
            # print(Tests[measurement_type].value, value, is_safe)
            status.append(is_safe)

        returnItem = Area(name=name, quality=WaterQuality.Bad)
        if Advice.Unsafe not in status:
            returnItem.quality = WaterQuality.Good
        return returnItem

    def is_value_safe(self, item, value):
        type_limit = {
            "E_COLI": 1800,
            "INTTNLETRCCN": 400
        }

        if value < type_limit[item]:
            return Advice.Safe
        return Advice.Unsafe

if __name__ == "__main__":
    ZwemwaterNL().info()
