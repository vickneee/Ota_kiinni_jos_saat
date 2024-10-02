from geopy.distance import geodesic as GD

from airport_table import get_airports, airports_location, get_recommended_airports
from past_movement_table import add_player_past_movement
from player_management import get_players_info, game_screen_names, update_location
from tickets_table import delete_ticket


def ai_criminal_move(name):
    # Get all airports and their locations
    all_airports = get_airports()
    all_airports_location = airports_location()

    # Get fugitive's current location
    criminal_info = get_players_info(name)
    criminal_id = criminal_info.get('id')
    criminal_location = criminal_info.get('location')
    #criminal_coords = all_airports_location[criminal_location]

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

    # Prepare ticket options based on the recommended airports
    sorted_airports = sorted(recommended_airports.items(), key=lambda x: x[1]['distance'])
    ticket_options = {
        'potkurikone': sorted_airports[:2],       # Two closest airports
        'matkustajakone': sorted_airports[2:4],   # 3rd and 4th closest airports
        'yksityskone': sorted_airports[-2:],      # Two farthest airports
    }

    best_total_distance = -1
    best_ticket_type = None
    best_destination_code = None

    # Find the best destination among possible options
    for ticket_type, possible_destinations in ticket_options.items():
        for code, info in possible_destinations:
            coords = all_airports_location[code]
            distance_to_detective1 = GD(coords, detective1_coords).kilometers
            distance_to_detective2 = GD(coords, detective2_coords).kilometers
            total_distance = distance_to_detective1 + distance_to_detective2

            if total_distance > best_total_distance:
                best_total_distance = total_distance
                best_ticket_type = ticket_type
                best_destination_code = code

    # Get destination details
    destination_info = all_airports[best_destination_code]
    add_player_past_movement(best_ticket_type, criminal_id,criminal_location)
    update_location(best_destination_code,name)
    #delete_ticket(best_ticket_type,criminal_info('player_id'))


    #sql = f"UPDATE player SET location = '{best_destination_code}' WHERE screen_name = {name}"


    return {
        'ticket_type': best_ticket_type,
        'airport_code': best_destination_code,
        'name': destination_info['name'],
        'country': destination_info['country'],
        'distance_from_criminal': recommended_airports[best_destination_code]['distance'],
        'distance_from_detective1': GD(all_airports_location[best_destination_code], detective1_coords).kilometers,
        'distance_from_detective2': GD(all_airports_location[best_destination_code], detective2_coords).kilometers,
        'total_distance_from_detectives': best_total_distance
    }

print(ai_criminal_move('kakkapylly'))