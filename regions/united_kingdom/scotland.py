from regions.region import Region

class Scotland(Region):

    def __init__(self):
        Region.__init__(self, 'gb-sct', 'England')
    
    def ingest(self):
        pass
