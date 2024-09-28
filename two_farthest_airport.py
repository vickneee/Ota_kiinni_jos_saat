# Description: Find two farthest airports from criminal's starting point
from geopy.units import km

from airport_table import get_airports, print_airports
from player_table import get_criminal_info
from math import radians, cos, sin, asin, sqrt


# Haversine formula to calculate the distance between two points on the Earth
def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of Earth in kilometers
    return c * r


def two_farthest_airport(name):
    airports = get_airports()
    farthest_airports = [None, None]
    max_distance = 0
    second_max_distance = 0
    starting_point = get_criminal_info(name)

    for icao, location in airports.items():
        distance = haversine(starting_point['latitude'], starting_point['longitude'], location['latitude'], location['longitude'])
        if distance > max_distance:
            second_max_distance = max_distance
            max_distance = distance
            farthest_airports[1] = farthest_airports[0]
            farthest_airports[0] = (icao, location['name'], location['country'], f"{distance:.2f} km")
        elif distance > second_max_distance:
            second_max_distance = distance
            farthest_airports[1] = (icao, location['name'], location['country'], f"{distance:.2f} km")

    return farthest_airports


# Test the function
print(two_farthest_airport("Äiti"))

