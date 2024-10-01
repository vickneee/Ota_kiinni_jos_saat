import os
from airport_table import get_airports, print_airports, get_recommended_airports, print_recommended_airports
from assisting_functions import tyhj


def player_move(name):
    print("Kaikki lentokentät:")

    # Print all available airports
    airports = get_airports()
    print_airports(airports)

    # Get recommended airports for the player
    recommended_airports = get_recommended_airports(name)

    # Print recommended airports using the name parameter (sorted from farthest to nearest)
    print("Suositellut lentokentät:")
    print_recommended_airports(name)  # This function handles sorting and printing

    # Extract keys for indexing from recommended_airports
    recommended_keys = list(recommended_airports.keys())  # Get keys directly from the dictionary

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
                    f"""Valitsit lentokentän: 
                {selected_airport['country']} : {selected_airport['name']} - {selected_airport['distance']:.2f} km""")
                break  # Exit loop if input is valid
            else:
                print("Virheellinen valinta. Yritä uudelleen.")
        except ValueError:
            print("Virheellinen syöte. Syötä numero.")

    tyhj()

    return selected_airport  # Return the selected airport information


# Example call to the function
player_move("Janne")
