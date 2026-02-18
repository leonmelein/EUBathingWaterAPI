from regions.region import Region

class Estonia(Region):

    def __init__(self):
        Region.__init__(self, 'EE', 'Estonia')

    def ingest(self):
        pass