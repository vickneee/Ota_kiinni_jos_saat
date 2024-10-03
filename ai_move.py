from geopy.distance import geodesic as GD
from past_movement_table import add_player_past_movement
from tickets_table import delete_ticket
import random


def ai_criminal_move(name):
    from airport_table import get_airports, airports_location, get_recommended_airports
    from player_management import get_players_info, game_screen_names, update_location
    # Get all airports and their locations
    all_airports = get_airports()
    all_airports_location = airports_location()

    # Get fugitive's current location
    criminal_info = get_players_info(name)
    criminal_id = criminal_info.get('id')
    criminal_location = criminal_info.get('location')

    # Get detectives' locations
    detective_names = game_screen_names()
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
    destination_info = all_airports[best_destination_code]

    # Update player's movement and location
    add_player_past_movement(best_ticket_type, criminal_id, criminal_location)
    update_location(best_destination_code, name)
    # Optionally delete the ticket if it's used
    #delete_ticket(best_ticket_type, criminal_id)


def ai_detective_move(criminal_name, detective_name):
    from airport_table import airports_location, get_recommended_airports
    from player_management import get_players_info, update_location
    # Rikollisen ja etsivien tiedot
    criminal_info = get_players_info(criminal_name)
    detective_info = get_players_info(detective_name)
    detective_id = detective_info.get('id')
    # Rikollisen ja etsivien sijainnit
    criminal_location = criminal_info.get('location')
    detective_location = detective_info.get('location')

    # Suositellut lentokentät etsivälle
    recommended_airports = get_recommended_airports(detective_name)

    # Laske jokaisen suositellun lentokentän etäisyys rikolliseen
    criminal_coords = airports_location()[criminal_location]
    airport_distances = {}

    for code, airport_info in recommended_airports.items():
        # Lasketaan lentokentän koordinaattien perusteella
        # etäisyys rikolliseen ja muutetaan kilometreiksi
        airport_coords = airports_location()[code]
        distance_to_criminal = f"{GD.distance(criminal_coords, airport_coords).kilometers:.2f}"
        airport_distances[code] = distance_to_criminal

        # Lentokentät suodatetaan etäisyyden mukaan
        # ja valitaan kolme lähintä lentokenttää rikolliseen nähden
    if len(airport_distances) < 3:
        closest_three = sorted(airport_distances.items())
    else:
        closest_three = sorted(airport_distances.items(), key=lambda x: x[1])[:3]

    chosen_airport_code = random.choice(closest_three)[0]
    chosen_airport = recommended_airports[chosen_airport_code]
    update_location(chosen_airport_code, detective_name)
    delete_ticket(chosen_airport['ticket_type'], detective_id)
