from regions.region import Region
import pandas as pd
import requests

class Malta(Region):

    def __init__(self):
        Region.__init__(self, 'mt', 'Malta')

    def ingest(self):
        data = fetch_bathing_sites()
        df = pd.json_normalize(data['features'])
        df = df.drop_duplicates(subset=['attributes.Site_Code'])

        dataset = df[[
            'attributes.Site_Code',
            'attributes.Name_ENG',
            'geometry.x',
            'geometry.y'
        ]]
        dataset.rename(mapper={
            'attributes.Site_Code': 'id',
            'attributes.Name_ENG': 'name',
            'geometry.x': 'lon',
            'geometry.y': 'lat'
        }, axis=1, inplace=True)

        self._processLocationList(dataset)
        self._processIndividualLocations(dataset)
        return dataset


def fetch_bathing_sites():
    url = (
        "https://utility.arcgis.com/usrsvcs/servers/"
        "7535042c1bf84078a5af5e14acb7604d/rest/services/"
        "EHD_BathingSitesJoined_PublicView_/FeatureServer/0/query"
    )

    params = {
        "f": "pjson",
        "outFields": (
            "BC_Class,Bathing_Water_Profile,Blue_Flag_OR_Beach_of_Quality,Description,"
            "EU_Class,Local_Council,Name_ENG,Name_MT,Pet_Friendly,Press_Release_Link,"
            "RecommendedForBathing_YES_OR_NO,Remarks,Sandy_OR_Rocky_Beach,Site_Code,"
            "Zone,ObjectId,GlobalID"
        ),
        "outSR": "4326 ",
        "returnM": "true",
        "returnZ": "true",
        "spatialRel": "esriSpatialRelIntersects",
        "where": "1=1",
    }

    headers = {
        "accept": "*/*",
        "accept-language": "nl,en;q=0.9",
        "cache-control": "no-cache",
        "origin": "https://mfh-mt.maps.arcgis.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://mfh-mt.maps.arcgis.com/apps/dashboards/31f48638f89c4d60bd6143818a46a2c7",
        'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
        "sec-ch-ua-mobile": "?0",
        'sec-ch-ua-platform': '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
    }

    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()
