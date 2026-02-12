from requests import get, Request
import geopandas as gpd
from pathlib import Path
from json import dump
import logging

class Region():
    def __init__(self, iso_code, country, region=None):
        self.iso_code = iso_code
        self.country = country
        self.region = region

        if region == None:
            self.filepath = f'data/{self.iso_code}'
            Path(f'{self.filepath}/locations').mkdir(exist_ok=True, parents=True)

        self.log = logging.getLogger("EUBathingWaterAPI")

    def description(self):
        if self.region is None:
            return f'{self.country}'
        else:
            return f"{self.country} - {self.region}"

    def loadJSON(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }
        self.log.info(f'{self.description()} - Loading URL: {url}')
        return get(url, headers=headers).json();

    def loadWFSLayer(self, layer_name, wfs_url, method='GET',):
        params = dict(service='WFS', version="2.0.0", request='GetFeature',
                            typeName=layer_name, outputFormat='json', srsName="EPSG:4326")
        
        wfs_request_url = Request(method, wfs_url, params=params).prepare().url
        self.log.info(f'{self.description()} - Loading layer: {layer_name} ({wfs_url})')
        return gpd.read_file(wfs_request_url) # type: ignore
    
    def _processLocationList(self, data):
        # All locations per region
        data.to_json(f'{self.filepath}/locations.json', orient="records", mode="w")

    def _processIndividualLocations(self, data):
        # Individual location data
        self.log.info(f'{self.description()} - Item count: {data.shape[0]}')

        for id, row in data.iterrows():
            row_dict = row.to_dict()
            filename = f'{self.filepath}/locations/{id}.json'
            with open(filename, 'w+') as f:
                dump(row_dict, f, indent=2)