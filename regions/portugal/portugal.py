from regions.region import Region
from io import StringIO
import requests
import pandas as pd

class Portugal(Region):
    url = "https://snirh.apambiente.pt/snirh/_dadossintese/zbalnear/xml/xml_praiasano.php?ano=2024&novoConc=&site=&entidade=&dadosrecentes=0&praiascomdadosxdias=0&simples=1"

    def __init__(self):
        Region.__init__(self, 'pt', 'Portugal')

    def ingest(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        }
        data = requests.get(self.url, headers=headers).text

        df = pd.read_xml(
            StringIO(data)
        )
        
        df = pd.read_xml(StringIO(data))
        df = df[[
            "site", "nome", "lng", "lat"
        ]]
        df.rename(mapper={
            "site": "id",
            "nome": "name",
            "lng": "lon"
        }, axis=1, inplace=True)
        df['name'] = df['name'].str.title()

        self._processLocationList(df)
        self._processIndividualLocations(df)
        return df