# Estonia

| Properties |      |
|------------|------|
| ISO Code   | `EE` |
| Regional   | No   |
| Type       | XML  |

## Issues
- Not all locations have GPS coordinates

## Format
Data is in XML format. See [XSD specification](./supluskohad.xml).

## Fields

- The specification has been automatically translated. Please beware of any translation errors.
- Items like the coordinates or sampling location are nested elements. Pandas does not automatically read those elements using `read_xml(...)`


| Field                                     | Description                                                                                                                                                                               | Data Type | Cardinality |
|-------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|-------------|
| **id**                                    | Bathing site ID in the system                                                                                                                                                             | Integer   | 1           |
| **nimetus**                               | Bathing site name                                                                                                                                                                         | String    | 1           |
| **supluskoha_grupi_id**                   | Bathing site group ID                                                                                                                                                                     | String    | 0–1         |
| **tyyp**                                  | Bathing site type (bathing site / public water body)                                                                                                                                      | String    | 1           |
| **supluskoha_avaandmete_URL**             | Bathing site open data link                                                                                                                                                               | String    | 1           |
| **suplusvee_profiili_URL**                | Bathing water profile URL; refers to the bathing water profile location in VTI open data                                                                                                  | String    | 0–1         |
| **aadress**                               | Address                                                                                                                                                                                   | String    | 0–1         |
| **koordinaadid**                          | Bathing site coordinates                                                                                                                                                                  |           | 0–1         |
| → **koordinaat**                          | Coordinate                                                                                                                                                                                |           | 0–N         |
| →→ **x**                                  | X coordinate                                                                                                                                                                              | Number    | 1           |
| →→ **y**                                  | Y coordinate                                                                                                                                                                              | Number    | 1           |
| **veekogu_nimi**                          | Name of the water body                                                                                                                                                                    | String    | 0–1         |
| **veekogu_tyyp**                          | Type of water body                                                                                                                                                                        | String    | 0–1         |
| **kylastajate_arv**                       | Estimated maximum number of visitors during the bathing season                                                                                                                            | Integer   | 0–1         |
| **rannajoone_pikkus**                     | Shoreline length                                                                                                                                                                          | Integer   | 0–1         |
| **supluskoha_piirjooned**                 | Bathing site boundary lines                                                                                                                                                               | String    | 0–1         |
| **seirekalendri_kooskolastamise_kuupaev** | Monitoring calendar approval date (d.m.Y)                                                                                                                                                 | Date      | 0–1         |
| **viimane_inspekteerimine**               | Date of last inspection (d.m.Y)                                                                                                                                                           | Date      | 0–1         |
| **inspekteerija**                         | Name of the last inspector                                                                                                                                                                | String    | 0–1         |
| **viimane_proovivott**                    | Date of last sampling (d.m.Y)                                                                                                                                                             | Date      | 0–1         |
| **veekvaliteet**                          | Water quality (very good / average / poor)                                                                                                                                                | String    | 0–1         |
| **suplusvee_kvaliteediklass**             | Bathing water quality class. Possible values:  <br>• very good  <br>• good  <br>• sufficient  <br>• poor  <br>• not possible to assess  <br>• new  <br>• sampling frequency non-compliant | String    | 0–1         |
| **proovivotu_metoodikad**                 | List of sampling methodologies                                                                                                                                                            |           | 0–N         |
| → **proovivotu_metoodika**                | Sampling methodology                                                                                                                                                                      | String    | 1           |
| **proovivotuprotokolli_number**           | Sampling protocol number                                                                                                                                                                  | String    | 1           |
| **kaaskirja_number**                      | Sampling cover letter number                                                                                                                                                              | String    | 0–1         |
| **proovivotja_amet**                      | Sampler’s position/title                                                                                                                                                                  | String    | 0–1         |
| **proovivotukohad**                       | Related sampling locations                                                                                                                                                                |           | 0–1         |
| → **proovivotukoht**                      | Sampling location                                                                                                                                                                         |           | 0–N         |
| →→ **id**                                 | Sampling location ID                                                                                                                                                                      | Integer   | 1           |
| →→ **nimi**                               | Sampling location name                                                                                                                                                                    | String    | 1           |
| →→ **aadress**                            | Sampling location address                                                                                                                                                                 | String    | 1           |
| →→ **koordinaadid**                       | Sampling location coordinates                                                                                                                                                             |           | 0–1         |
| →→→ **koordinaat**                        | Coordinate                                                                                                                                                                                |           | 0–N         |
| →→→→ **x**                                | X coordinate                                                                                                                                                                              | Number    | 1           |
| →→→→ **y**                                | Y coordinate                                                                                                                                                                              | Number    | 1           |
| →→ **veeallika_liik**                     | Type of water source                                                                                                                                                                      | String    | 0–1         |
| →→ **proovivotukoha_liik**                | Type of sampling location                                                                                                                                                                 | String    | 0–1         |
| →→ **proovivotukoha_liigitus**            | Classification of sampling location                                                                                                                                                       | String    | 0–1         |
| **inspektori_kommentaarid**               | Inspector’s comments                                                                                                                                                                      | String    | 0–1         |

