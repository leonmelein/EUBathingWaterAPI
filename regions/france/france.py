from regions.region import Region
from dotenv import load_dotenv
from itertools import islice
import pandas as pd
import os
import requests
import warnings


class France(Region):
    indexUrl = "https://sigmas.social.gouv.fr/server/rest/services/baignades/fra_vue_baignade/MapServer/5/query?f=json&where=1%3D1&returnIdsOnly=true&geometry=-9678710.360800,-28545813.431743,30099965.362980,42759085.476384&geometryType=esriGeometryEnvelope&spatialRel=esriSpatialRelEnvelopeIntersects"

    def __init__(self, proxy=True):
        Region.__init__(self, 'fr', 'France')
        load_dotenv()
        self.proxy = proxy
        if self.proxy:
            self.socks_proxy = os.getenv('PROXY')

    def ingest(self):
        session = requests.Session()
        proxies = {
            'http' : f'socks5h://{self.socks_proxy}',
            'https' : f'socks5h://{self.socks_proxy}',
        }

        if not self.socks_proxy:
            warnings.warn("No proxy provided. Please use a French IP address to connect to these resources.")
            proxies = {}
        
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        headers = {'user-agent' : user_agent}

        locationIdResponse = session.get(self.indexUrl, headers=headers, proxies=proxies).json()
        idList = locationIdResponse['objectIds']
        print(len(idList))
        
        # Slice up list in parts of 100
        it = iter(idList) 
        n = 100
        res = [list(islice(it, n)) for _ in range((len(idList) + n - 1) // n)]

        dataset = []
        for item in res:
            # Stringify IDs to include them in the request
            item = [str(x) for x in item]
            ids = ",".join(item) 
            data = session.get(f"https://sigmas.social.gouv.fr/server/rest/services/baignades/fra_vue_baignade/MapServer/5/query?f=geojson&objectIds={ids}&inSR&outSR&returnGeometry=true&outFields=*&returnM=false&returnZ=false", headers=headers, proxies=proxies).json()
            dataset = dataset  + data['features']

        df = pd.json_normalize(dataset)
        df = df[[
            "properties.OBJECTID",
            "properties.lsite",
            "geometry.coordinates"
        ]]
        df.rename(mapper={
            "properties.OBJECTID": "id",
            "properties.lsite": "name",
            "geometry.coordinates": "coordinates"
        }, axis=1, inplace=True)
        df['lon'] = [item[0] for item in df['coordinates']]
        df['lat'] = [item[1] for item in df['coordinates']]
        df['name'] = df['name'].str.title()
        df.drop(labels=["coordinates"], axis=1, inplace=True)
        
        self._processLocationList(df)
        self._processIndividualLocations(df)
        return df