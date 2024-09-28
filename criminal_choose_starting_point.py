from airport_table import print_airports, get_airports
from db_functions import db_insert
from player_table import insert_player


# Karkurin valitsee oman aloituspaikan kaikista mahdollisista lentokentistä ja sijainneista
# Choose starting point for the criminal from all possible airports and locations
def criminal_choose_starting_point():
    # Karkuri valitsee aloituspaikan
    print("Karkuri valitsee aloituspaikan")
    print_airports(get_airports())
    airports = get_airports()
    choose = int(input("Valitse aloituspaikka (1-21): "))
    selected_icao = list(airports.keys())[choose - 1]
    location = airports[selected_icao]
    print(f"Karkuri on valinnut aloituspaikakseen lentokentän numero {choose}.")
    print(f"""Lentokenttä: {location['name']}, Maa: {location['country']}, Sijainti: ({location['latitude']}, {location['longitude']})""")
    # Karkurin aloituspaikan tallentaminen tietokantaan
    # Insert the criminal's starting point into the database
    name = "Karkuri"
    type = 0
    icao_code = selected_icao  # ICAO code of the airport where the criminal starts the game
    # Call function insert_player from player_table.py
    insert_player(name, type, icao_code)
    # SQL query
    sql = f"""INSERT INTO player (screen_name, type, location) 
    VALUES ('{name}', {type}, '{icao_code}')"""
    # Execute SQL query
    add = db_insert(sql)

    return choose


