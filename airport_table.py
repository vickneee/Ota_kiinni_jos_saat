from db_functions import db_query
from assisting_functions import haversine
from geopy.distance import geodesic as GD


# Fetch 21 airports from the database
def get_airports():
    airports = {}
    icao_codes = ('EFHK', 'ENGM', 'EGLL',
                  'LFPG', 'LEMD', 'EDDB',
                  'LIRF', 'LPPT', 'EIDW',
                  'LOWW', 'LGAV', 'EBBR',
                  'ESSA', 'EPWA', 'LHBP',
                  'LROP', 'LKPR', 'LYBE',
                  'BIKF', 'LBSF', 'UKBB')
    sql = f"""select airport.ident, airport.name, country.name, airport.latitude_deg, airport.longitude_deg 
    from airport inner join country on airport.iso_country = country.iso_country 
    where ident in {icao_codes}"""
    result = db_query(sql)
    for row in result:
        airports[row[0]] = {"name": row[1], "country": row[2], "latitude": row[3], "longitude": row[4]}

    return airports


# Function to print the airports
def print_airports(airports):
    for i in range(1, 22):
        icao = list(airports.keys())[i - 1]
        print(f"{i}. {airports[icao]['country']} : {airports[icao]['name']}")


# Get the location of the airports and put them in a dictionary
def airports_location():
    airports_location = {}
    all_airports = get_airports()
    for key, value in all_airports.items():
        airports_location[key] = (value['latitude'], value['longitude'])
    return airports_location


# Get the six(or less depending on remaining tickets) recommended airports for the player, sorted by distance
def get_recommended_airports(name):
    from player_management import get_players_info
    from tickets_table import player_tickets
    all_airports = get_airports()
    player = get_players_info(name)
    player_id = player.get('id')
    tickets = player_tickets(player_id)
    all_airports_location = airports_location()
    player_location = all_airports_location[player['location']]
    airport_distances = {}

    for key, value in all_airports_location.items():
        if key != player['location']:
            airport_distances[key] = GD(player_location, value).kilometers

    all_sorted_locations = sorted(airport_distances.items(), key=lambda x: x[1])
    #print(all_sorted_locations)
    recommended = {}
    if 'potkurikone' in tickets.keys() :
        for key, value in all_sorted_locations[:2]:
            recommended[key] = {"name": all_airports[key]['name'], "country": all_airports[key]['country'],
                                "distance": value,"ticket_type": 'potkurikone'}
    if 'matkustajakone' in tickets.keys():
        for key, value in all_sorted_locations[2:4]:
            recommended[key] = {"name": all_airports[key]['name'], "country": all_airports[key]['country'],
                            "distance": value, "ticket_type": 'matkustajakone'}
    if 'yksityiskone' in tickets.keys():
        for key, value in all_sorted_locations[-2:]:
            recommended[key] = {"name": all_airports[key]['name'], "country": all_airports[key]['country'],
                            "distance": value, "ticket_type": 'yksityiskone'}

    return recommended


# Print the recommended airports for the player
def print_recommended_airports(name):
    recommended = get_recommended_airports(name)

    # Sort the recommended airports by distance
    sorted_airports = sorted(recommended.items(), key=lambda x: x[1]['distance'])

    print("Mahdolliset lentokentät lähimmästä kauimpaan:")
    for i, (key, value) in enumerate(sorted_airports[:6], start=1):
        print(f"{i}. {value['country']} : {value['name']} - lipputyyppi : {value['ticket_type']}")

    return sorted_airports


def two_farthest_airport(name):
    from player_management import get_players_info
    airports = get_airports()
    farthest_airports = [None, None]
    max_distance = 0
    second_max_distance = 0
    starting_point = get_players_info(name)

    for icao, location in airports.items():
        distance = haversine(starting_point['latitude'], starting_point['longitude'], location['latitude'],
                             location['longitude'])
        if distance > max_distance:
            second_max_distance = max_distance
            max_distance = distance
            farthest_airports[1] = farthest_airports[0]
            farthest_airports[0] = (icao, location['name'], location['country'], f"{distance:.2f} km")
        elif distance > second_max_distance:
            second_max_distance = distance
            farthest_airports[1] = (icao, location['name'], location['country'], f"{distance:.2f} km")

    return farthest_airports
