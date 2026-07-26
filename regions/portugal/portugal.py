from io import BytesIO

import pandas as pd
import requests

from regions.region import Region


class Portugal(Region):
    url = "https://snirh.apambiente.pt/snirh/_dadossintese/zbalnear/xml/xml_praiasano.php?ano=2025&novoConc=&site=&entidade=&dadosrecentes=0&praiascomdadosxdias=0&simples=1"

    def __init__(self):
        Region.__init__(self, 'pt', 'Portugal')
        print("WARNING: RUN WITH VPN")

    def ingest(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        }
        data = requests.get(self.url, headers=headers)

        df = pd.read_xml(BytesIO(data.content))
        df = df[[
            "site", "nome", "lng", "lat"
        ]]
        df.rename(mapper={
            "site": "id",
            "nome": "name",
            "lng": "lon"
        }, axis=1, inplace=True)
        df['name'] = df['name'].str.title()
        df['country'] = self.iso_code

        self._processLocationList(df)
        self._processIndividualLocations(df)
        return df