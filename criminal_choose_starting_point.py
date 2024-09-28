from airport_table import print_airports, get_airports
from player_table import insert_player


# Karkurin valitsee oman aloituspaikan kaikista mahdollisista lentokentistä ja sijainneista
# Choose starting point for the criminal from all possible airports and locations
def criminal_choose_starting_point(name):
    # Karkuri valitsee aloituspaikan
    print("Karkuri valitsee aloituspaikan")
    print_airports(get_airports())
    airports = get_airports()
    choose = int(input("Valitse aloituspaikka (1-21): "))
    selected_icao = list(airports.keys())[choose - 1]
    location = airports[selected_icao]
    print(f"Karkuri on valinnut aloituspaikakseen lentokentän numero {choose}.")
    print(f"""Lentokenttä: {location['name']}, Maa: {location['country']}, Sijainti: ({location['latitude']}, {location['longitude']})""")
    #insert the player into the database
    add = insert_player(name, 0, selected_icao)


    return add


