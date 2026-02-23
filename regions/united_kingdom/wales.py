from regions.region import Region
import pandas as pd

class Wales(Region):
    url = "https://environment.data.gov.uk/wales/bathing-waters/doc/bathing-water?_pageSize=1000&_view=bathing-water&_properties=latestProfile.countyName.name%2Cdistrict.alias%2ClatestSampleAssessment.followingSuspension.endOfSuspension%2ClatestSampleAssessment.sampleDateTime.ordinalYear%2ClatestComplianceAssessment.sampleYear.ordinalYear%2ClatestComplianceAssessment.assessmentQualifier%2ClatestComplianceAssessment.assessmentRegime&_lang=en%2Ccy%2Cnone"

    def __init__(self):
        Region.__init__(self, 'gb-cym', 'United Kingdom', 'Wales')
    
    def ingest(self):
        data = self.loadJSON(self.url)
        df = pd.json_normalize(data['result']['items'])
        df = df.rename(columns={
            "eubwidNotation": "id",
            "name._value": "name",
            "samplingPoint.lat": "lat",
            "samplingPoint.long": "lon"
        })
        df = df[["id", "name", "lat", "lon"]]
        return df
