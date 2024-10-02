from airport_table import get_airports, print_airports, get_recommended_airports, print_recommended_airports
from player_management import update_location, get_players_info
from tickets_table import player_tickets, delete_ticket


def player_move(name):
    print("Kaikki lentokentät:")

    # Print all available airports
    airports = get_airports()
    print_airports(airports)

    # Get recommended airports for the player
    recommended_airports = get_recommended_airports(name)

    get_players_info(name)
    player_id = get_players_info(name).get('id')
    # print(player_id)
    available_tickets = player_tickets(player_id)
    # print(available_tickets)
    print("Sinulla on seuraavat lentoliput:")
    for key, value in available_tickets.items():
        print(f"{key}: {value} kpl")

    # Print recommended airports using the name parameter (sorted from farthest to nearest)
    print_recommended_airports(name)  # This function handles sorting and printing

    # Extract keys for indexing from recommended_airports
    recommended_keys = list(recommended_airports.keys())  # Get keys directly from the dictionary
    print(recommended_keys)  # Print the keys for debugging

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
    # print(location)
    update_location(location, name)

    # Update the ticket count
    ticket_type = selected_airport['ticket_type']
    print(ticket_type)
    # print(ticket_type)
    delete_ticket(ticket_type, player_id)
    # print(player_tickets(player_id))


# Example call to the function
player_move("Kimmo")
