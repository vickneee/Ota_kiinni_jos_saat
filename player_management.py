from termcolor import colored

from db_functions import db_query, db_insert, db_update
from tickets_table import insert_tickets
import random

# Function to insert a new player into the database
def insert_player(name, type, location, is_computer=0):
    sql = f"""INSERT INTO player (screen_name, type, location, is_computer)
              VALUES ('{name}', '{type}', '{location}', {is_computer})"""
    add = db_insert(sql)
    return add

# Function to add a player to a game
def add_player_game(player_id, game_id):
    sql = f"""insert into game_player (game_id,player_id) 
    values ('{game_id}', '{player_id}')"""
    add = db_insert(sql)

# Function to get player information by screen name
def get_players_info(name):
    sql = f"""
        select player.id, player.screen_name, player.type,player.is_computer,player.location, airport.name, country.name,airport.latitude_deg, airport.longitude_deg 
        from player 
        left join airport on player.location = airport.ident 
        left join country on airport.iso_country = country.iso_country 
        where screen_name = '{name}'
    """
    result = db_query(sql)
    player_info = {}
    if result:
        player_info["id"] = result[0][0]
        player_info["screen_name"] = result[0][1]
        player_info["type"] = result[0][2]
        player_info["is_computer"] = result[0][3]
        player_info["location"] = result[0][4]
        player_info["airport_name"] = result[0][5]
        player_info["country_name"] = result[0][6]
        player_info["latitude"] = result[0][7]
        player_info["longitude"] = result[0][8]
    return player_info


# Function to get all screen names of players
def screen_names():
    sql = "select screen_name from player"
    result = db_query(sql)
    names = []
    for row in result:
        names.append(row[0])
    return names

def game_screen_names(game_id):
    sql = f"""select screen_name from player left join game_player on player.id = game_player.player_id 
    left join game on game_player.game_id = game.id where game.id = '{game_id}'"""
    result = db_query(sql)
    names = []
    for row in result:
        names.append(row[0])
    return names[-2:]

# Function to get screen names of players in a specific game
def all_game_screen_names(game_id):
    sql = f"""select screen_name from player left join game_player on player.id = game_player.player_id 
        left join game on game_player.game_id = game.id where game.id = '{game_id}'"""
    result = db_query(sql)
    names = []
    for row in result:
        names.append(row[0])
    return names

# Function to get the latest movement of a criminal
def get_criminal_movements(player_id):
    info = {}
    sql = f"""
    SELECT player.screen_name,airport.name,country.name, past_movement.ticket_type
    FROM past_movement
    LEFT JOIN player ON past_movement.player_id = player.id
    LEFT JOIN airport ON past_movement.location = airport.ident
    LEFT JOIN country ON airport.iso_country = country.iso_country
    WHERE past_movement.player_id = '{player_id}'
    ORDER BY past_movement.id DESC
    LIMIT 1
    """
    criminal_movement=db_query(sql)
    info["screen_name"] = criminal_movement[0][0]
    info["airport"] = criminal_movement[0][1]
    info["country"] = criminal_movement[0][2]
    info["ticket_type"] = criminal_movement[0][3]
    return info




# Function to prompt for a new player name and validate it
def new_player(type):
    names = screen_names()
    max_char = 20

    role = "rikollisen" if type == 0 else "etsivän"
    while True:
        name = input(f"Syötä {role} nimimerkki: ")
        if name not in names and name and len(name) <= max_char:
            print(f"Nimimerkki {name} lisätty.")
            return name
        elif not name:
            print(colored("Tyhjä nimimerkki. Yritä uudelleen!","red"))
        elif len(name) > max_char:
            print(colored(f"Nimimerkin on oltava enintään {max_char} merkkiä pitkä.","red"))
        elif name in names:
            print(colored("Nimimerkki on varattu. Valitse uusi.","red"))

# Function to insert tickets for a player based on their type
def insert_player_tickets(player_id, player_type):
    if player_type == 0:
        for i in range(10):
            insert_tickets(player_id, "potkurikone")
        for i in range(6):
            insert_tickets(player_id, "matkustajakone")
        for i in range(4):
            insert_tickets(player_id, "yksityiskone")
    else:
        for i in range(5):
            insert_tickets(player_id, "potkurikone")
        for i in range(3):
            insert_tickets(player_id, "matkustajakone")
        for i in range(2):
            insert_tickets(player_id, "yksityiskone")



# Function for the criminal to choose a starting point
def criminal_choose_starting_point(name, is_computer=0):
    # Karkuri valitsee aloituspaikan
    from airport_table import print_airports, get_airports
    from assisting_functions import tyhj
    airports = get_airports()
    if is_computer:
        selected_icao = random.choice(list(airports.keys()))
    else:
        print("Rikollinen valitsee aloituspaikan")
        print_airports(get_airports())
        choose = int(input("Valitse aloituspaikka (1-21): "))
        while choose < 1 or choose > 21:
            print(colored("Virheellinen syöte. Valitse aloituspaikka (1-21): ","red"))
            choose = int(input("Valitse aloituspaikka (1-21): "))

        selected_icao = list(airports.keys())[choose - 1]
        location = airports[selected_icao]
        print(f"Rikollinen on valinnut aloituspaikakseen lentokentän numero {choose}.")
        print(f"Lentokenttä: {location['name']}, Maa: {location['country']}, Sijainti: ({location['latitude']}, {location['longitude']})")
    tyhj()
    #insert the player into the database
    add = insert_player(name, 0, selected_icao, is_computer)
    insert_player_tickets(add, 0)
    return add

# Function to update the location of a player
def update_location(location, name):
    sql = f"""
    UPDATE player
    SET location = '{location}'
    WHERE screen_name = '{name}'
    """
    db_update(sql)

# Function to show the locations of detectives
def show_detective_locations():
    detective_names = game_screen_names()
    detective1_name = detective_names[0]
    detective2_name = detective_names[1]
    detective1_info = get_players_info(detective1_name)
    detective2_info = get_players_info(detective2_name)
    print(f"Etsivän {detective1_name} sijainti: {detective1_info['country_name']}, {detective1_info['airport_name']}")
    print(f"Etsivän {detective2_name} sijainti: {detective2_info['country_name']}, {detective2_info['airport_name']}")

