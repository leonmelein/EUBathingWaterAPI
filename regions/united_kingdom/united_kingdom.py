from regions.region import Region
from regions.united_kingdom.england import England
from regions.united_kingdom.wales import Wales
from regions.united_kingdom.scotland import Scotland
from regions.united_kingdom.northern_ireland import NorthernIreland

from tqdm import tqdm
from pandas import concat

class UnitedKingdom(Region):
    def __init__(self):
        Region.__init__(self, 'uk', 'United Kingdom')

    def ingest(self):
        regions = [
            England(),
            Wales(),
            Scotland(),
            NorthernIreland()
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
