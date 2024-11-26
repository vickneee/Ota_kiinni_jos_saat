from geopy.distance import geodesic as GD
from oldfiles.past_movement_table import add_player_past_movement
from oldfiles.tickets_table import delete_ticket
import random


def ai_criminal_move(name, game_id):
    from oldfiles.airport_table import airports_location, get_recommended_airports
    from oldfiles.player_management import get_players_info, game_screen_names, update_location
    # Get all airports and their locations
    # all_airports = get_airports()
    all_airports_location = airports_location()

    # Get fugitive's current location
    criminal_info = get_players_info(name)
    criminal_id = criminal_info.get('id')
    criminal_location = criminal_info.get('location')

    # Get detectives' locations
    detective_names = game_screen_names(game_id)
    detective1_name = detective_names[0]
    detective2_name = detective_names[1]
    detective1_info = get_players_info(detective1_name)
    detective2_info = get_players_info(detective2_name)
    detective1_coords = all_airports_location.get(detective1_info['location'])
    detective2_coords = all_airports_location.get(detective2_info['location'])

    # Get recommended airports for the fugitive
    recommended_airports = get_recommended_airports(name)

    best_total_distance = -1
    best_ticket_type = None
    best_destination_code = None

    # Find the best destination among possible options
    for airport_code, info in recommended_airports.items():
        ticket_type = info['ticket_type']
        coords = all_airports_location[airport_code]
        distance_to_detective1 = GD(coords, detective1_coords).kilometers
        distance_to_detective2 = GD(coords, detective2_coords).kilometers
        total_distance = distance_to_detective1 + distance_to_detective2

        # Choose the airport that maximizes distance from both detectives
        if total_distance > best_total_distance:
            best_total_distance = total_distance
            best_ticket_type = ticket_type
            best_destination_code = airport_code

    # Get destination details
    # destination_info = all_airports[best_destination_code]

    # Update player's movement and location
    add_player_past_movement(criminal_id, criminal_location, best_ticket_type)
    update_location(best_destination_code, name)


# Function of the detective's move
def ai_detective_move(criminal_name, detective_name):
    from oldfiles.airport_table import airports_location, get_recommended_airports
    from oldfiles.player_management import get_players_info, update_location
    # Criminal and Detectives information
    criminal_info = get_players_info(criminal_name)
    detective_info = get_players_info(detective_name)
    detective_id = detective_info.get('id')
    # Criminal and Detectives locations
    criminal_location = criminal_info.get('location')
    # detective_location = detective_info.get('location')

    # Recommended airports for detective
    recommended_airports = get_recommended_airports(detective_name)

    # Calculate every recommended airport's distance to the criminal
    criminal_coords = airports_location()[criminal_location]
    airport_distances = {}

    for code, airport_info in recommended_airports.items():
        # Calculate airport coordinates based on the airport's code
        # Distance to criminal and change it to kilometers
        airport_coords = airports_location()[code]
        distance_to_criminal = f"{GD(criminal_coords, airport_coords).kilometers:.2f}"
        airport_distances[code] = distance_to_criminal

        # Airports sorted by distance
        # And select three closest airports to the criminal
    if len(airport_distances) < 3:
        closest_three = sorted(airport_distances.items())
    else:
        closest_three = sorted(airport_distances.items(), key=lambda x: x[1])[:3]

    # Choose one of the three closest airports
    chosen_airport_code = random.choice(closest_three)[0]
    chosen_airport = recommended_airports[chosen_airport_code]
    update_location(chosen_airport_code, detective_name)
    delete_ticket(chosen_airport['ticket_type'], detective_id)
