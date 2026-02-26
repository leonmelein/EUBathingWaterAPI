import json
import pandas as pd

import requests
from bs4 import BeautifulSoup

from regions.region import Region

class Greece(Region):
    url = "https://bathingwaterprofiles.gr/en/bathing-waters-coast-map"

    def __init__(self):
        Region.__init__(self, 'gr', 'Greece')

    def ingest(self):
        data = requests.get(self.url)
        soup = BeautifulSoup(data.text, "html.parser")
        dataset = soup.find("script", attrs={"type": "application/json", "data-drupal-selector": "drupal-settings-json"})
        if not dataset:
            return pd.DataFrame()

        drupalJson = json.loads(dataset.text)
        df = pd.json_normalize(drupalJson['coastMap']['coast-map-69a01bf273704']['monitors'])
        df.rename(mapper={
            'title': 'id',
            'coast_name': 'name'
        }, axis=1, inplace=True)
        df = df[[
            'id', 'name', 'lat', 'lon'
        ]]
        
        self._processLocationList(df)
        self._processIndividualLocations(df)
        return df
    