from io import StringIO

import pandas as pd
import requests
from bs4 import BeautifulSoup

from regions.region import Region


class Hungary(Region):
    url = "https://nnk.gov.hu/index.php/kozegeszsegugyi-laboratoriumi-foosztaly/terkepes-informaciok/furdovizminosegi-terkep"
    type = "Scraping"

    def __init__(self):
        Region.__init__(self, 'hu', 'Hungary')

    def ingest(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "Cookie": ""
        }
        website = requests.get(self.url, headers=headers)

        soup = BeautifulSoup(website.text, "html.parser")
        table = soup.find_all("table")
        location_table = table[1]

        parsed_locations = pd.read_html(StringIO(location_table.prettify()))[0]
        df = parsed_locations.iloc[: , :-2]
        df.rename(mapper={
            "Szélesség, Hosszúság": "coordinates",
            "Helyszín": "name",
            "Mérés dátuma": "measurement_date",
            "Cím": "address",
            "Vízminőség": "quality"
        }, axis=1, inplace=True)
        df['lat'] = df['coordinates'].apply(lambda x: float(x.split(',')[0]))
        df['lon'] = df['coordinates'].apply(lambda x: float(x.split(',')[1]))

        df['id'] = self._syntheticIds(len(df))
        df = df[[
            'id', 'name', 'lat', 'lon'
        ]]
        df['country'] = self.iso_code

        self._processLocationList(df)
        self._processIndividualLocations(df)
        return df

    def _syntheticIds(self, length):
        return [f'HU000{i}' for i in range(1, length + 1)]