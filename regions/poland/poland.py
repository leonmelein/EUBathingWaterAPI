import re

import json5
import pandas as pd
import requests
from bs4 import BeautifulSoup

from regions.region import Region


class Poland(Region):
    url = 'https://sk.gis.gov.pl/kapieliska/mapa'

    def __init__(self, cookies):
        Region.__init__(self, 'pl', "Poland")
        self.cookies = cookies

    def ingest(self):
        if self.cookies:
            headers = {
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
                    "Cookie": ""
            }
            website = requests.get(self.url, headers=headers)
            soup = BeautifulSoup(website.text, "html.parser")
        else:
            with open('./regions/poland/mapa.html', 'r') as webpage:
                soup = BeautifulSoup(webpage, "html.parser")

        scripts = soup.find_all("script")
        map = scripts[-2].text

        regex = r"var markers = (\[\n.*\],\n.\s\s\s\s\s\s\s\s\s\s\s\s\])"
        test = re.search(regex, map, re.DOTALL)
        
        if test:
            scraped_data = json5.loads(test.group(1))
        else:
            return None
        
        df = pd.DataFrame(
            scraped_data, # type: ignore
            columns=["lon", "lat", "html", "color"]
        )

        df['name'] = df.apply(self._collect_name, axis=1)
        df['alternate_name'] = df.apply(lambda x: x['name'], axis=1)
        df['id'] = df.apply(self._collect_id, axis=1)
        df['url'] = df.apply(self._collect_url, axis=1)
        df = df[["id", "name", "alternate_name", "lat", "lon"]]
        df['country'] = self.iso_code

        self._processLocationList(df)
        self._processIndividualLocations(df)
        return df


    def _collect_name(self, row):
        name_pattern = r"<div><b>(.*)</b></div>"
        flag_pattern = r"&#x1F6A9;"

        name = re.findall(name_pattern, row['html'])
        name = name[0].strip()
        name = re.sub(flag_pattern, '', name)
        name = re.sub('\"', '', name)

        return name

    def _collect_url(self, row):
        url_pattern = r"https:\/\/sk.gis.gov.pl\/kapielisko\/\d+"
        url = re.findall(url_pattern, row['html'])
        
        return url[0]

    def _collect_id(self, row):
        url = self._collect_url(row)
        if len(url) > 0:
            return url.split('/')[4]
        else:
            return ''

    def _collect_status(self, row):
        status = True
        unsuitable = "nieprzydatna"

        if row['html'].find(unsuitable) > 0:
            status = False
        return status

