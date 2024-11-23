from backend.game_functions.assisting_functions import haversine
from geopy.distance import geodesic as GD
from database import Database

# Define airport class
class Airport:
    def __init__(self, ident, name, country, latitude, longitude):
        self.ident = ident
        self.name = name
        self.country = country
        self.latitude = latitude
        self.longitude = longitude

    # Fetch 21 airports from the database
    def get_airports(self, database):
        airports = {}
        icao_codes = ('EFHK', 'ENGM', 'EGLL', 'LFPG', 'LEMD', 'EDDB', 'LIRF', 'LPPT', 'EIDW', 'LOWW', 'LGAV', 'EBBR',
                      'ESSA', 'EPWA', 'LHBP', 'LROP', 'LKPR', 'LYBE', 'BIKF', 'LBSF', 'UKBB')
        sql = f"""SELECT airport.ident, airport.name, country.name, airport.latitude_deg, airport.longitude_deg 
                  FROM airport 
                  INNER JOIN country ON airport.iso_country = country.iso_country 
                  WHERE ident IN {icao_codes}"""

        result = database.db_query(sql)
        for row in result:
            airports[row[0]] = {"name": row[1], "country": row[2], "latitude": row[3], "longitude": row[4]}

        return airports

    # Get locations (latitude and longitude) from all airports
    def airports_location(self, database):
        airports_location_dict = {}
        airports = self.get_airports(database)

        for key, value in airports.items():
            airports_location_dict[key] = (value['latitude'], value['longitude'])

        return airports_location_dict

    # Get recommended airports based on the players location and ticket types
    def get_recommended_airports(self, player_location, tickets, player_type, database):
        airport_locations = self.airports_location(database)
        player_lat_lon = (player_location['latitude'], player_location['longitude'])

        airport_distances = {}

        for icao, location in airport_locations.items():
            if icao != player_location['location']:
                airport_distances[icao] = GD(player_lat_lon, location).kilometers

        sorted_distances = sorted(airport_distances.items(), key=lambda x: x[1])

        recommended = {}

        # Add recommended airports for each ticket type
        if 'potkurikone' in tickets:
            for key, value in sorted_distances[:2]:  # Limit to first 2
                recommended[key] = {"name": airport_locations[key]['name'], "country": airport_locations[key]['country'],
                                    "distance": value, "ticket_type": 'potkurikone'}

        if 'matkustajakone' in tickets:
            for key, value in sorted_distances[2:4]:  # Next 2
                recommended[key] = {"name": airport_locations[key]['name'], "country": airport_locations[key]['country'],
                                    "distance": value, "ticket_type": 'matkustajakone'}

        if player_type == 0 and 'yksityiskone' in tickets:
            for key, value in sorted_distances[-2:]:  # Last 2 airports
                recommended[key] = {"name": airport_locations[key]['name'], "country": airport_locations[key]['country'],
                                    "distance": value, "ticket_type": 'yksityiskone'}

        return recommended

    # Find two farthest airports from players location
    def two_farthest_airports(self, player_location, database):
        airports = self.get_airports(database)
        farthest_airports = [None, None]
        max_distance = 0
        second_max_distance = 0

        # Iterate through all airports to find the farthest ones
        for icao, location in airports.items():
            distance = haversine(player_location['latitude'], player_location['longitude'],
                                 location['latitude'], location['longitude'])

            # Update the farthest and second farthest airports
            if distance > max_distance:
                second_max_distance = max_distance
                max_distance = distance
                farthest_airports[1] = farthest_airports[0]
                farthest_airports[0] = (icao, location['name'], location['country'], f"{distance:.2f} km")
            elif distance > second_max_distance:
                second_max_distance = distance
                farthest_airports[1] = (icao, location['name'], location['country'], f"{distance:.2f} km")

        return farthest_airports
