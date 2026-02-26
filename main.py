from tqdm import tqdm
from datetime import datetime
from pandas import concat
import colorama
import logging
import time
import json
from numpy import nan
from geojson import Feature, Point, FeatureCollection, dump

from regions import *

class Ingester():
    def __init__(self, regionProviders, generateEU=False,):
        self.regions = regionProviders
        self.generateEU = generateEU

        # Logging
        logFormatter = logging.Formatter("%(levelname)s %(asctime)s EUBathingWaterAPI %(message)s")
        fileHandler = logging.FileHandler("{0}".format('latest.log'))
        fileHandler.setFormatter(logFormatter)

        rootLogger = logging.getLogger('EUBathingWaterAPI')
        rootLogger.addHandler(fileHandler)
        rootLogger.setLevel(logging.INFO)
        self.log = rootLogger

        # Set up color support in Terminal
        colorama.init()
        
    def ingest(self):
        self._preStep()

        dataset = []
        progressBar = tqdm(self.regions, desc="Region", unit='region', colour='green')
        for region in progressBar:
            progressBar.set_description(region.description(), refresh=True)
            data = region.ingest()

            # If generating EU wide list, add to dataset
            if self.generateEU:
                dataset.append(data)

        # EU wide list of locations
        if self.generateEU:
            eu_data = concat(dataset)
            eu_data.to_json('data/locations.json', orient="records", mode="w")

            # GeoJSON generation
            collection = []
            for _, item in eu_data.iterrows():
                if item['lat'] is not nan and item['lon'] is not nan:
                    feature = Feature(
                        # id=item['id'],
                        geometry=Point((item['lon'], item['lat'])),
                        properties={
                            "name": item['name']
                        }
                    )
                    collection.append(feature)
            
            with open("data/locations.geojson", "w", encoding="utf-8") as f:
                data = FeatureCollection(collection, bbox=[35.537814,-29.623947,71.499216,41.567459])
                dump(data, f, ensure_ascii=False)
                    
        self._postStep()

    def _preStep(self):
        self.time = time.process_time()
        print(colorama.Fore.BLUE + colorama.Style.BRIGHT +
              "⭐️ EU Bathing Water API\n"
             f"Run date: {datetime.now()}")
        self.log.info(msg=f"Start run: {datetime.now()}")

    def _postStep(self):
        self.log.info(msg=f"End run: {datetime.now()}")
        self.log.info(msg=f"Time elapsed: {time.process_time() - self.time}")
        self.startTime, self.endTime = None, None
        print("Done!")

if __name__ == "__main__":
    regions = [
        Netherlands(),
        Belgium(),
        Germany(),
        Austria(),
        Switzerland(),
        Luxembourg(),
        # Poland(),
        Lithuania(),
        Sweden(),
        Denmark(),
        Czechia(),
        Slovakia(),
        Hungary(),
        UnitedKingdom(),
        Croatia(),
        Latvia(),
        Ireland(),
        Estonia(),
        Greece()
    ]
    # regions =[Germany()]
    loader = Ingester(regions, generateEU=True)
    loader.ingest()
