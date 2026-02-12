from regions.region import Region

class Netherlands(Region):
    url = "https://pubgeo.zwemwater.nl/geoserver/zwr_public/wfs"

    def __init__(self):
        Region.__init__(self, "nl", "Netherlands")

    # Function to concatenate values only if both columns have non-missing values
    def _address_concat(self, row):
        col1 = row['street'].strip()
        col2 = row['adr_woonplaats'].strip()
        if col1 and col2:
            return f"{col1}, {col2}"
        else:
            if len(col2.strip()) > 0:
                return col2
            return ""


    def ingest(self):
        # Base Data
        zwemplekken = self.loadWFSLayer("zwr_public:zwemplekken", self.url)
        zwemplekken = zwemplekken.drop(columns=['id', 'datum']).set_index('key_id')
        zwemplekken.drop_duplicates(subset=['zwemwaterlocatie_id'], inplace=True)

        zwemplekken_details = self.loadWFSLayer("zwr_public:zwemplekken_details", self.url)
        zwemplekken_details = zwemplekken_details.drop(columns=["id", "info_id", "geometry", "datum"])
        zwemplekken_details['adr_huisnummer'] = zwemplekken_details['adr_huisnummer'].astype('Int64')
        zwemplekken_details[['adr_huisletter', 'adr_huisnummertoevoeging', 'adr_straat']] = zwemplekken_details[['adr_huisletter', 'adr_huisnummertoevoeging', 'adr_straat']].fillna('')
        zwemplekken_details[['adr_straat', 'adr_huisnummer', 'adr_huisletter', 'adr_huisnummertoevoeging']].astype(str)
        zwemplekken_details['adr_huisnummer'] = zwemplekken_details['adr_huisnummer'].astype(str).replace('<NA>','')
        zwemplekken_details['adr_postcode'] = zwemplekken_details['adr_postcode'].fillna('')
        zwemplekken_details['adr_woonplaats'] = zwemplekken_details['adr_woonplaats'].fillna('')
        zwemplekken_details['street'] = (
            zwemplekken_details['adr_straat'].fillna('').astype(str).str.strip()
            .str.cat(
                zwemplekken_details[
                    ['adr_huisnummer', 'adr_huisletter', 'adr_huisnummertoevoeging']
                ]
                .fillna('')
                .astype(str)
                .apply(lambda c: c.str.strip()),
                sep=' ',
            )
            .str.replace(r'\s+', ' ', regex=True)
            .str.strip()
            .str.title()
        )

        zwemplekken_details['address'] = zwemplekken_details.apply(self._address_concat, axis=1)
        zwemplekken_details.drop(columns=['adr_huisnummer', 'adr_huisletter', 'adr_huisnummertoevoeging', 'adr_straat', 'adr_postcode', 'street'], inplace=True)
        zwemplekken_details.drop_duplicates(subset=['zwemwaterlocatie_id'], inplace=True)

        base_data = zwemplekken_details.copy()
        base_data = base_data[["zwemwaterlocatie_id", "naam", "korte_naam", "address", "adr_woonplaats", "status", "tekst", "info_filename", "website"]]

        zwemplekdata = base_data.merge(zwemplekken, left_on="zwemwaterlocatie_id", right_on="zwemwaterlocatie_id", how="left")
        zwemplekdata['lat'] = zwemplekdata['geometry'].apply(lambda geom: geom.y if geom else None)
        zwemplekdata['lon'] = zwemplekdata['geometry'].apply(lambda geom: geom.x if geom else None)
        zwemplekdata = zwemplekdata.drop(columns=["korte_naam_x", "naam_x", "status_x", "geometry"])
        zwemplekdata = zwemplekdata.rename(columns={
            "naam_y": "naam",
            "korte_naam_y": "korte_naam",
            "status_y": "status"
        })
        zwemplekdata.sort_values(by=["naam"], inplace=True)
        
        # Pictures
        # EU designations
        # eu_designations = loadWFSLayer("zwr_public:eustatussen", self.url)
        # eu_designations = eu_designations[eu_designations['jaar'] == 2024].drop(columns=['type_eu_status_id', 'geometry', 'omschrijving', 'id'])
        # eu_current_designations = eu_designations.drop(columns=["key_id", "jaar"])
        # data = zwemplekdata.merge(eu_current_designations, left_on="zwemwaterlocatie_id", right_on="zwemwaterlocatie_id", how="left")
        # data.fillna({'code': 0}, inplace=True)

        # Measurements
        # measurements = loadWFSLayer("zwr_public:resultaatsen", self.url)
        # measurements = measurements.drop(columns=['id', 'datum_geplande_monstername', 'monitoring_datum_id', 'monitoring_plan_id', 'monster_id', 'type_object_id', 'geometry'])
        # measurements = measurements.sort_values(["zwemwaterlocatie_id", "object_begin_tijd", "type_object_code"])
        # measurements = measurements.drop_duplicates(subset=["zwemwaterlocatie_id", "type_object_code"], keep="last")
        # measure = measurements.pivot_table(values='numerieke_waarde', index='zwemwaterlocatie_id', columns='type_object_code')
        # data = data.merge(measure, on="zwemwaterlocatie_id", how="left")

        # Amenities
        # zwemplek_voorziening = loadWFSLayer("zwr_public:zwemplek_voorziening", self.url)
        # voorzieningen = zwemplek_voorziening.groupby('zwemwaterlocatie_id')['voorziening_type_id'].agg(list).reset_index()
        # data = data.merge(voorzieningen, on="zwemwaterlocatie_id", how="left")
        data = zwemplekdata # TODO: remove
        data.rename(columns={
            "zwemwaterlocatie_id": "id",
            "naam": "name",
            "korte_naam": "alternate_name",
            "adr_woonplaats": "placename",
            "status": "current_status",
            "tekst": "description",
            "info_filename": "photos",
            "code": "eu_designation",
            "E_COLI": "e_coli",
            "INTTNLETRCCN": "int_ent",
            "voorziening_type_id": "voorzieningen"
        }, inplace=True)
        data.set_index("id", inplace=True)
        data['name'] = data['name']\
            .str.strip()\
            .str.title()\
            .str.replace("Ij", "IJ", regex=True)\
            .str.replace("^Rcn", "RCN", regex=True)\
            .str.replace("^T ", "'t ", regex=True)\
            .str.replace("['|`]T ", "'t ", regex=True)\
            .str.replace("['|`]S", "'s", regex=True)
        data['alternate_name'] = data['alternate_name']\
            .str.strip()\
            .str.title()\
            .str.replace("^Rcn", "RCN", regex=True)\
            .str.replace("^T ", "'t ", regex=True)\
            .str.replace("['|`]T ", "'t ", regex=True)\
            .str.replace("['|`]S", "'s", regex=True)
        
        # Active Warnings
        # preventative_measures = loadWFSLayer("zwr_public:zwemplek_maatregel", self.url)
        # preventative_measures = preventative_measures.drop(columns=['id', 'bw_code', 'object_type', 'toelichtingstandaardextended', 'type', 'geometry', 'zwemplek_naam'])
        # active_warnings = preventative_measures[(preventative_measures['objectbegintijd'] <= '2025-06-13')]
        # active_warnings = active_warnings.drop(columns=['redeningetrokken', 'objectbegintijd', 'objecteindtijd', 'omschrijving', 'key_id'])
        # active_warnings = active_warnings[[
        #     'zwemwaterlocatie_id', 'toelichtingstandaard', 'toelichtingpubliek']
        # ]
        # active_warnings.set_index('zwemwaterlocatie_id', inplace=True)
        # active_warnings.rename(columns={
        #     'toelichtingstandaard': 'warning_type',
        #     'toelichtingpubliek': 'warning_description'
        # }, inplace=True)
        # warnings = active_warnings.groupby(['zwemwaterlocatie_id'])[['warning_type','warning_description']].apply(lambda x: x.to_dict('records')).reset_index(name='warnings')

        # data = data.merge(warnings, on="zwemwaterlocatie_id", how="left")
        # data.rename(columns={
        #     "zwemwaterlocatie_id": "id",
        #     "voorzieningen": "amenities"
        # }, inplace=True)
        # data['amenities'] = data['amenities'].apply(lambda x: list(set(x)) if isinstance(x, (list, set, tuple)) else list())
        # data['warnings'] = data['warnings'].apply(lambda x: x if isinstance(x, (list, set, tuple)) else list())
        # data.fillna({'e_coli': 0}, inplace=True)
        # data.fillna({'int_ent': 0}, inplace=True)

        finalData = data[[
            'name', 'alternate_name', 'lat', 'lon'
        ]]

        self._processLocationList(finalData)
        self._processIndividualLocations(finalData)
        # Final reshaping
        return finalData