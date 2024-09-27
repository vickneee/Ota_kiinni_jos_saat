from airport_table import get_airports
from db_functions import db_query

# Karkurin valitsee oman aloituspaikan kaikista mahdollisista lentokentistä ja sijainneista


def criminal_choose_starting_point():
    # Karkuri valitsee aloituspaikan
    print("Karkuri valitsee aloituspaikan")
    airports = get_airports()
    choose = int(input("Valitse aloituspaikka (1-21): "))
    selected_icao = list(airports.keys())[choose - 1]
    selected_airport = airports[selected_icao]
    print(f"Karkuri on valinnut aloituspaikakseen lentokentän numero {choose}.")
    print(f"""Lentokenttä: {selected_airport['name']}, Sijainti: ({selected_airport['latitude']}, {selected_airport['longitude']})""")
    return choose


criminal_choose_starting_point()
