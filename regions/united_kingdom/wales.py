from regions.region import Region

class Wales(Region):

    def __init__(self):
        Region.__init__(self, 'gb-cym', 'England')
    
    def ingest(self):
        pass
