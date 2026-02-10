from regions.region import Region
from regions.belgium.flanders import Flanders
from regions.belgium.wallonia import Wallonia
from tqdm import tqdm
from pandas import concat


class Belgium(Region):
    def __init__(self):
        Region.__init__(self, "be", "Belgium")
    
    def ingest(self):
        regions = [
            Flanders(),
            Wallonia()
        ]

        data = []
        progressBar = tqdm(regions)
        for region in progressBar:
            progressBar.set_description(region.description(), refresh=True)
            regionalData = region.ingest()
            data.append(regionalData)

        dataset = concat(data)

        self._processLocationList(dataset)
        self._processIndividualLocations(dataset)

        return dataset
