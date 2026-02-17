from regions.region import Region

class NorthernIreland(Region):

    def __init__(self):
        Region.__init__(self, 'gb-nir', 'Northern Ireland')
    
    def ingest(self):
        pass
