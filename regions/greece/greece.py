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
        coast_map = drupalJson.get("coastMap", {})
        coast_map_key = next((k for k in coast_map if k.startswith("coast-map-")), None)
        if not coast_map_key:
            return pd.DataFrame()

        df = pd.json_normalize(coast_map[coast_map_key].get("monitors", []))
        if df.empty:
            return pd.DataFrame()
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
    
