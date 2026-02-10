# Netherlands
Source: 

# Zwemwater.nl Signaalwaarden
| EC    | IE    |
| ----- | ----- |
| 1800  | 400   |

# Swimspot

| Name              | Type          | Values                        |
|-------------------|---------------|-------------------------------|
| name              | string        |                               |
| alternate_name    | string        |                               |
| lat               | float         |                               |
| lon               | float         |                               |
| description       | string        |                               |
| url               | string        | <http://www.zwemwater.nl/#101/> |
| features          | [feature]     |                               |
| eu_designation    | int           | {null, 0...3}                 |
| current_status    | string        |                               |
| e_coli            | int           |                               |
| int_ent           | int           |                               |
| comfort           | int           |                               |
| water_temperature | float         | 20.0                          |
| photos            | [url: string] | []                            |

## Feature

| id | description                  | symbol                 |
|----|------------------------------|------------------------|
| 1  | Public Transport             | public_transport       |
| 2  | Speeltuin                    | playing_area           |
| 3  | Douches                      | shower                 |
| 4  | Toiletten                    | toilet                 |
| 5  | Afvalbak                     | bins                   |
| 6  | Speelweide                   | play_field             |
| 7  | Ligweide                     | sunbathing             |
| 8  | Honden toegestaan            | dogs_allowed           |
| 9  | Afdrijfgevaar                | danger                 |
| 10 | EHBO                         | first_aid              |
| 11 | Fietsenstalling              | bike_parking           |
| 12 | bereikbaar_met_ov            | public_transport_v2    |
| 13 | speeltoestellen              | playing_area           |
| 14 | douches                      | shower                 |
| 15 | wc_toiletten                 | toilet                 |
| 16 | afvalbakken                  | bins                   |
| 17 | speelweide                   | play_field             |
| 18 | ligweide                     | sunbathing_area        |
| 19 | honden_toegelaten            | dogs_allowed           |
| 20 | honden_toegestaan            | dogs_allowed           |
| 21 | afdrijvingsgevaar            | danger                 |
| 22 | ehbo                         | first_aid              |
| 23 | fietsenstalling              | bike_parking_v2        |
| 24 | horeca                       | restaurant             |
| 25 | jetski_mogelijkheid          | Jetski                 |
| 26 | jetski_mogelijkheden         | Jetski                 |
| 27 | kleedruimte                  | changing_room          |
| 28 | surf_mogelijkheid            | wind_surfing           |
| 29 | surf_mogelijkheden           | wind_surfing           |
| 30 | parkeergelegenheid           | parking_v2             |
| 31 | entreeheffing                | paid_entrance          |
| 32 | toegankelijk_voor_invaliden  | accessible_to_disabled |
| 33 | strandrolstoel               | accessible_to_disabled |
| 34 | voorzieningen_voor_invaliden | accessible_to_disabled |
| 35 | aflopende_bodem              | slope                  |
| 36 | trailerhelling               | trailer                |
| 37 | infobord                     | information_sign       |
| 38 | kitesurf_mogelijkheden       | kite_surfing           |
| 39 | reddingsbrigade              | lifeguard              |
| 40 | naaktstrand                  | nude_beach_v2          |
| 41 | zout_water                   | salt_water             |
| 42 | zoet_water                   | sweet_water            |
| 43 | teken_aanwezig               | ticks                  |
| 44 | getijdewater                 | tidal_water            |
| 45 | zandstrand                   | sand_beach             |
| 46 | diepte_zwemlocatie           | water_level            |
| 47 | drijflijn                    | line                   |
| 48 | surf_mogelijkheden           | wind_surfing           |
| 49 | blauwe_vlag                  | blue_flag              |
| 50 | toezicht_categorie_c         | toezicht_c             |
| 51 | uitkijkpost                  | observation_tower      |
| 52 | duiktoren                    | diving_tower           |
| 53 | strandhuis                   | beach_house            |
| 54 | waterglijbaan                | water_slide            |
| 55 | doorzicht                    | doorzicht              |
| 56 | toezicht_categorie_d         | toezicht_d             |

## EU Status

| id | description | symbol |
|----|-------------|--------|
| 0  | Poor        | -      |
| 1  | Sufficient  | ★      |
| 2  | Good        | ★★     |
| 3  | Excellent   | ★★★    |
