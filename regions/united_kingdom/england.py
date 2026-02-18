from regions.region import Region

import pandas as pd

class England(Region):
    url = "https://environment.data.gov.uk/doc/bathing-water?_pageSize=1000&_view=bathing-water&_properties=latestProfile.countyName.name%2Cdistrict.alias%2ClatestSampleAssessment.sampleDateTime.ordinalYear%2ClatestComplianceAssessment.sampleYear.ordinalYear%2ClatestComplianceAssessment.assessmentQualifier%2ClatestComplianceAssessment.assessmentRegime&_lang=en%2Ccy%2Cnone&country=http%3A%2F%2Fdata.ordnancesurvey.co.uk%2Fid%2Fcountry%2Fengland&_query-id=XbY01NFqXbY"

    def __init__(self):
        Region.__init__(self, 'gb-eng', 'England')
    
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