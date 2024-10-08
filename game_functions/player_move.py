from termcolor import colored
from game_functions.assisting_functions import clear
from game_functions.tickets_table import player_tickets, delete_ticket,print_available_tickets
from game_functions.past_movement_table import add_player_past_movement


# Function to handle player movement
def player_move(name, round, player_ids, screen_names):
    from game_functions.airport_table import get_airports, print_airports, get_recommended_airports, print_recommended_airports
    from game_functions.player_management import update_location, get_players_info, get_criminal_movements

    print(colored("Kaikki lentokentät:", "green"))

    # Print all available airports
    airports = get_airports()
    print_airports(airports)
    criminal_id = player_ids[0]

    # Get recommended airports for the player
    recommended_airports = get_recommended_airports(name)

    # Get player information
    get_players_info(name)
    player_id = get_players_info(name).get('id')
    player_type = get_players_info(name).get('type')
    old_location = get_players_info(name).get('location')
    # Get available tickets for the player
    available_tickets = player_tickets(player_id)
    # print(available_tickets)
    print("")
    print(colored(f"Pelin kierros: {round}\n", "green"))

    print_available_tickets(available_tickets)

    print("")

    # If player is criminal print detective locations
    if player_type == 0:

        for detective in screen_names[1:]:
            detective_info = get_players_info(detective)
            print(f"Etsivän {detective_info.get('screen_name')} sijainti: {detective_info.get('airport_name')}, {detective_info.get('country_name')}")

    # If player is detective print criminal location depending on round
    if player_type == 1 and round in [2,3,5,6,8,9]:
        criminal_info = get_criminal_movements(criminal_id)

        print(f"Rikollisen {criminal_info.get('screen_name')} viimeksi käytetty lippu: {criminal_info.get('ticket_type')}")

    if player_type == 1 and round in [1, 4, 7, 10]:
        criminal_info = get_criminal_movements(criminal_id)

        print(f"Rikollisen {criminal_info.get('screen_name')} viime sijainti: {criminal_info.get('airport')}, {criminal_info.get('country')} käytetty lippu: {criminal_info.get('ticket_type')}")

    print("")
    print(f"Sinun vuorosi {get_players_info(name).get('screen_name')}, Sijaintisi: {get_players_info(name).get('airport_name')}, {get_players_info(name).get('country_name')}\n")

    # Print recommended airports using the name parameter (sorted from farthest to nearest)
    print_recommended_airports(name)  # This function handles sorting and printing

    # Extract keys for indexing from recommended_airports
    recommended_keys = list(recommended_airports.keys())  # Get keys directly from the dictionary

    # Ask the player to select an airport
    while True:
        try:
            selected_index = input(colored(f"Valitse lentokenttä (1-{len(recommended_keys)}): ", "green"))  # Prompt user for selection
            if selected_index == "x":
                return selected_index
            else:
                selected_index = int(selected_index)
            if 1 <= selected_index <= len(recommended_keys):
                selected_key = recommended_keys[selected_index - 1]  # Get the corresponding key
                selected_airport = recommended_airports[selected_key]  # Get the airport details using the key

                # Print exact airport details
                print(
                    f"Valitsit lentokentän: {selected_airport['country']} : {selected_airport['name']} ja käytit {selected_airport['ticket_type']} lentolipun.")
                break  # Exit loop if input is valid
            else:
                print(colored("Virheellinen valinta. Yritä uudelleen.", "red"))
        except ValueError:
            print(colored("Virheellinen syöte. Syötä numero.", "red"))
    if selected_index != "x":
        # Update the player location
        new_location = selected_key  # Get the location of the selected airport
        update_location(new_location, name)

        # Update the ticket type
        ticket_type = selected_airport['ticket_type']

        # Add the player's past movement to the database
        if player_type == 0:
            add_player_past_movement(player_id, old_location, ticket_type)
        else:
            delete_ticket(ticket_type, player_id)

        clear()
    return selected_index

