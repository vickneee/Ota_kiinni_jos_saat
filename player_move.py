from airport_table import get_airports, print_recommended_airports, get_recommended_airports, print_airports
from db_functions import db_insert
from past_movement_table import add_player_past_movement
from player_management import screen_names


def player_move(name):
    # Update the player's location
    print("Kaikki lentokentät:")
    print_airports(airports=get_airports())
    print_recommended_airports(name)
    numero = int(input("Valitse lentokenttä: "))
    recommended_airports = get_recommended_airports(name)
    lista = []
    for key, value in recommended_airports.items():
        list.append(key)
    if numero not in lista:
        print("Valitse jokin suositelluista lentokentistä")
        return False
    else:
        print(f"Valitsit lentokentän: {recommended_airports[numero][1]['name']}")

    # Update the player's location
    db_insert(f"UPDATE player SET location = {iaoc} WHERE name = '{name}'")

    # # Add the ticket and player information to the database
    # add = add_player_past_movement(ticket_type, player_id, new_location)
    # if not add:
    #     return False
    #
    # return add


player_move("Janne")
