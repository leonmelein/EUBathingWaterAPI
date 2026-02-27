from requests import get, Request
import geopandas as gpd
from pathlib import Path
from json import dump
from numpy import nan
from geojson import Feature, Point, FeatureCollection, dump as geodump
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
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01"
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
        data.to_json(f'{self.filepath}/locations.json', orient="records", mode="w", force_ascii=False)
        # GeoJSON generation
        collection = []
        for _, item in data.iterrows():
            if item['lat'] is not nan and item['lon'] is not nan:
                feature = Feature(
                    # id=item['id'],
                    geometry=Point((item['lon'], item['lat'])),
                    properties={
                        "name": item['name']
                    }
                )
                collection.append(feature)
        
        with open(f"{self.filepath}/locations.geojson", "w", encoding="utf-8") as f:
            data = FeatureCollection(collection, bbox=[35.537814,-29.623947,71.499216,41.567459])
            geodump(data, f, ensure_ascii=False)

    def _processIndividualLocations(self, data):
        # Individual location data
        self.log.info(f'{self.description()} - Item count: {data.shape[0]}')

        for id, row in data.iterrows():
            row_dict = row.to_dict()
            name = id
            try:
                name = row['id']
            except:
                pass
        
            filename = f'{self.filepath}/locations/{name}.json'
            with open(filename, 'w+') as f:
                dump(row_dict, f, indent=2, ensure_ascii=False)