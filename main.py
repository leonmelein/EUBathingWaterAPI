from tqdm import tqdm
from datetime import datetime
from pandas import concat
import colorama
import logging
import time
import json

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

            geojson = {
                "type": "FeatureCollection",
                "features": []
            }

            # TODO: replace with actual robust encoding
            for _, item in eu_data.iterrows():
                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [item["lon"], item["lat"]]
                    },
                    "properties": {
                        k: v for k, v in item.items() if k not in ("lat", "lon")
                    }
                }
                geojson["features"].append(feature)

            with open("data/locations.geojson", "w", encoding="utf-8") as f:
                json.dump(geojson, f, ensure_ascii=False, indent=2)
                    
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
        Austria(),
        Switzerland(),
        Luxembourg(),
        # Poland()
        Lithuania()
    ]
    loader = Ingester(regions, generateEU=True)
    loader.ingest()
