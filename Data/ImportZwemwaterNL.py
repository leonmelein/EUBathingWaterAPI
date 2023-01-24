import requests
import pandas as pd
import sqlite3
con = sqlite3.connect("data.db")

server = 'https://pubgeo.zwemwater.nl/geoserver/zwr_public/wfs'
body = f"""
        <GetFeature xmlns="http://www.opengis.net/wfs" service="WFS" version="1.1.0" outputFormat="application/json" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <Query typeName="zwr_public:resultaatsen" srsName="EPSG:28992" xmlns:zwr_public="https://pubgeo.zwemwater.nl/geoserver/zwr_public">
                </Query>
            </GetFeature>
        """
response = requests.post(server, body)
details = [item['properties'] for item in response.json()["features"]]

df = pd.DataFrame(details)
df['object_begin_tijd'] = pd.to_datetime(
    df['object_begin_tijd'], format='%Y-%m-%dT%H:%M:%SZ')
df = df.drop([
    "datum_geplande_monstername",
    "monitoring_plan_id",
    "monitoring_datum_id",
    "type_object_id",
    "key_id"
], axis=1)


cur = con.cursor()
for index, row in df.iterrows():
    cur.execute(f"""
    INSERT INTO measurements VALUES(
        '{row['monster_id']}', 
        '{row['zwemwaterlocatie_id']}',
        '{row['object_begin_tijd']}',
        '{row['type_object_code']}',x
        '{row['numerieke_waarde']}'
    )
""")
con.commit()