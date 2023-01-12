import requests
from Models.Area import Area
from Models.WaterQuality import WaterQuality


class MarineTerrein:
    def retrieve(self):
        url = 'https://www.marineterrein.nl/wp-json/mtnc/v1/sensors'
        data = requests.get(url).json()
        return Area("Marineterrein",
                    self.convert_quality(data['waterkwaliteit']),
                    float(data['watertemperatuur']))

    def convert_quality(self, quality):
        if quality == 'goed':
            return WaterQuality.Good
        elif quality == 'slecht':
            return WaterQuality.Bad
        else:
            return WaterQuality.Fair
