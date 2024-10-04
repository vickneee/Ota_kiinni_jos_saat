import os
from assisting_functions import tyhj
from tickets_table import player_tickets, delete_ticket
from past_movement_table import add_player_past_movement


def player_move(name, round, player_ids, screen_names):
    from airport_table import get_airports, print_airports, get_recommended_airports, print_recommended_airports
    from player_management import update_location, get_players_info, get_criminal_movements

    print("Kaikki lentokentät:")

    # Print all available airports
    airports = get_airports()
    print_airports(airports)
    criminal_id = player_ids[0]

    # Get recommended airports for the player
    recommended_airports = get_recommended_airports(name)

    get_players_info(name)
    player_id = get_players_info(name).get('id')
    player_type= get_players_info(name).get('type')

    # print(player_id)
    available_tickets = player_tickets(player_id)
    # print(available_tickets)
    print("")
    print(f"Pelin kierros: {round}\n")

    print("Sinulla on seuraavat lentoliput:")
    for key, value in available_tickets.items():
        print(f"{key}: {value} kpl")

    print("")

    if player_type == 0:

        for detective in screen_names[1:]:
            detective_info = get_players_info(detective)
            print(f"Etsivän {detective_info.get('screen_name')} sijainti: {detective_info.get('airport_name')}, {detective_info.get('country_name')}")

    #if player is detective print criminal location depending on round
    if player_type == 1 and round in [1,4,7,10]:
        criminal_info = get_criminal_movements(criminal_id)

        print(f"Rikollisen {criminal_info.get('screen_name')} viime sijainti: {criminal_info.get('airport')}, {criminal_info.get('country')} käytetty lippu: {criminal_info.get('ticket_type')}")

    print("")
    print(f"Sinun vuorosi {get_players_info(name).get('name')}, Sijaintisi: {get_players_info(name).get('airport_name')}, {get_players_info(name).get('country_name')}\n")

    # Print recommended airports using the name parameter (sorted from farthest to nearest)
    print_recommended_airports(name)  # This function handles sorting and printing

    # Extract keys for indexing from recommended_airports
    recommended_keys = list(recommended_airports.keys())  # Get keys directly from the dictionary

    #if player is criminal, detectives locations


    # Ask the player to select an airport
    while True:
        try:
            selected_index = int(
                input(f"Valitse lentokenttä (1-{len(recommended_keys)}): "))  # Prompt user for selection
            if 1 <= selected_index <= len(recommended_keys):
                selected_key = recommended_keys[selected_index - 1]  # Get the corresponding key
                selected_airport = recommended_airports[selected_key]  # Get the airport details using the key

                # Print exact airport details
                print(
                    f"Valitsit lentokentän: {selected_airport['country']} : {selected_airport['name']} ja käytit {selected_airport['ticket_type']} lentolipun.")
                break  # Exit loop if input is valid
            else:
                print("Virheellinen valinta. Yritä uudelleen.")
        except ValueError:
            print("Virheellinen syöte. Syötä numero.")

    # Update the player location
    location = selected_key  # Get the location of the selected airport

    update_location(location, name)

    # Update the ticket count
    ticket_type = selected_airport['ticket_type']

    if player_type == 0:
        add_player_past_movement(player_id, location, ticket_type)
    else:
        delete_ticket(ticket_type, player_id)


    tyhj()


# Example call to the function


