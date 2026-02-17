from regions.region import Region

class England(Region):

    def __init__(self):
        Region.__init__(self, 'gb-eng', 'England')
    
    def ingest(self):
        pass
