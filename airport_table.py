from db_functions import db_query
from player_table import get_players_info
from geopy.distance import geodesic as GD

#fetch 21 airports from the database
def get_airports():
    airports = {}
    icao_codes=('EFHK','ENGM','EGLL',
                'LFPG','LEMD','EDDB',
                'LIRF','LPPT','EIDW',
                'LOWW','LGAV','EBBR',
                'ESSA','EPWA','LHBP',
                'LROP','LKPR','LYBE',
                'BIKF','LBSF','UKBB')
    sql = f"select airport.ident, airport.name, country.name, airport.latitude_deg, airport.longitude_deg from airport inner join country on airport.iso_country = country.iso_country where ident in {icao_codes}"
    result = db_query(sql)
    for row in result:
        airports[row[0]] = {"name": row[1], "country": row[2], "latitude": row[3], "longitude": row[4]}

    return airports


#function to print the airports
def print_airports(airports):
    for i in range(1,22):
        icao = list(airports.keys())[i-1]
        print(f"{i}. {airports[icao]['country']} : {airports[icao]['name']}")

# get the location of the airports and put them in a dictionary
def airports_location():
    airports_location = {}
    all_airports = get_airports()
    for key, value in all_airports.items():
        airports_location[key] = (value['latitude'], value['longitude'])
    return airports_location

# get the six recommended airports for the player, sorted by distance
def get_recommended_airports(name):
    all_airports = get_airports()
    player = get_players_info(name)
    all_airports_location = airports_location()
    player_location = all_airports_location[player['location']]
    airport_distances = {}

    for key, value in all_airports_location.items():
        if key != player['location']:
            airport_distances[key] = GD(player_location, value).kilometers

    all_sorted_locations = sorted(airport_distances.items(), key=lambda x: x[1])
    recommended = {}
    for key, value in all_sorted_locations[:4]:
        recommended[key] = {"name": all_airports[key]['name'], "country": all_airports[key]['country'], "distance": value}
    for key, value in all_sorted_locations[-2:]:
        recommended[key] = {"name": all_airports[key]['name'], "country": all_airports[key]['country'], "distance": value}

    return recommended










