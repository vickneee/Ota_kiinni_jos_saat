from oldfiles.assisting_functions import haversine
from geopy.distance import geodesic as GD
from backend.game_functions.database import Database

# Define airport class
class Airport:

    # Fetch 21 airports from the database
    def get_airports(self):
        airports = {}
        icao_codes = ('EFHK', 'ENGM', 'EGLL', 'LFPG', 'LEMD', 'EDDB', 'LIRF', 'LPPT', 'EIDW', 'LOWW', 'LGAV', 'EBBR',
                      'ESSA', 'EPWA', 'LHBP', 'LROP', 'LKPR', 'LYBE', 'BIKF', 'LBSF', 'UKBB')
        sql = f"""SELECT airport.ident, airport.name, country.name, airport.latitude_deg, airport.longitude_deg 
                  FROM airport 
                  INNER JOIN country ON airport.iso_country = country.iso_country 
                  WHERE ident IN {icao_codes}"""

        result = Database().db_query(sql)
        for row in result:
            airports[row[0]] = {"name": row[1], "country": row[2], "latitude": row[3], "longitude": row[4]}

        return airports

    # Get locations (latitude and longitude) from all airports
    def airports_location(self):
        airports_location_dict = {}
        airports = self.get_airports()

        for key, value in airports.items():
            airports_location_dict[key] = (value['latitude'], value['longitude'])

        return airports_location_dict

    def airports_coord(self, icao):
        all_coord = self.airports_location()
        return all_coord[icao]

    # Get recommended airports based on the players location and ticket types
    def get_recommended_airports(self, name):
        from backend.game_functions.tickets import Tickets
        from backend.game_functions.player import Player
        all_airports = self.get_airports()
        all_airports_location = self.airports_location()
        player = Player.get_player_info(name)
        player_id = player.get('id')
        player_type = player.get('type')
        player_lat_lon = all_airports_location[player['location']]
        tickets = Tickets().player_tickets(player_id)
        airport_distances = {}

        for key, value in all_airports_location.items():
            if key != player['location']:
                airport_distances[key] = GD(player_lat_lon, value).kilometers

        sorted_distances = sorted(airport_distances.items(), key=lambda x: x[1])

        recommended = {}

        # Add recommended airports for each ticket type
        if 'potkurikone' in tickets:
            for key, value in sorted_distances[:2]:  # Limit to first 2
                recommended[key] = {"name": all_airports[key]['name'], "country": all_airports[key]['country'],
                                    "distance": value, "ticket_type": 'potkurikone', "latitude": all_airports[key][
                        'latitude'], "longitude": all_airports[key]['longitude'], "icao":key}
        if 'matkustajakone' in tickets:
            for key, value in sorted_distances[2:4]:  # Next 2
                recommended[key] = {"name": all_airports[key]['name'], "country": all_airports[key]['country'],
                                    "distance": value, "ticket_type": 'matkustajakone', "latitude": all_airports[key][
                        'latitude'], "longitude": all_airports[key]['longitude'], "icao":key}
        if 'yksityiskone' in tickets:
            for key, value in sorted_distances[-2:]:  # Last 2 airports
                recommended[key] = {"name": all_airports[key]['name'], "country": all_airports[key]['country'],
                                    "distance": value, "ticket_type": 'yksityiskone', "latitude": all_airports[key][
                        'latitude'], "longitude": all_airports[key]['longitude'], "icao":key}
        return recommended

    # Find two farthest airports from players location
    def two_farthest_airports(self, player_location):
        airports = self.get_airports()
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
                farthest_airports[0] = (icao, location['name'], location['country'], location['latitude'], location['longitude'], f"{distance:.2f} km")
            elif distance > second_max_distance:
                second_max_distance = distance
                farthest_airports[1] = (icao, location['name'], location['country'], location['latitude'], location['longitude'], f"{distance:.2f} km")

        return farthest_airports
