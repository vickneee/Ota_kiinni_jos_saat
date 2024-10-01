# EI toimi vielä!!!


from player_management import get_players_info
from airport_table import get_recommended_airports, airports_location
import random
import geopy.distance as GD

def ai_detective_move(criminal_name, detective_name):
        # Rikollisen ja etsivien tiedot
        criminal_info = get_players_info(criminal_name)
        detective_info = get_players_info(detective_name)

        # Rikollisen ja etsivien sijainnit
        criminal_location = criminal_info.get('location')
        detective_location = detective_info.get('location')

        # Suositellut lentokentät etsivälle
        recommended_airports = get_recommended_airports(detective_name)

        # Laske jokaisen suositellun lentokentän etäisyys rikolliseen
        criminal_coords = airports_location()[criminal_location]
        airport_distances = {}

        for code, airport_info in recommended_airports.items():
            # Lentokentän koordinaatit
            airport_coords = airports_location()[code]
            distance_to_criminal = GD.distance(criminal_coords, airport_coords).kilometers
            airport_distances[code] = distance_to_criminal

        # Lentokentät suodatetaan etäisyyden mukaan ja valitaan kolme lähintä
        closest_three = sorted(airport_distances.items(), key=lambda x: x[1])[:3]

        # Valitaan satunnaisesti yksi kolmesta lähimmästä lentokentästä
        chosen_airport_code = random.choice(closest_three)[0]
        chosen_airport = recommended_airports[chosen_airport_code]


        print(chosen_airport)
        return chosen_airport

ai_detective_move('jorma','pp')