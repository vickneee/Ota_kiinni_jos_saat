from db_functions import db_query, db_insert


# Player 1, choose your role: (0 or 1)
def player_choose_the_role():
    role_type = int(input("Valitse roolisi. Syötä 0 rikolliselle tai 1 etsijällä: "))
    while role_type != 0 or role_type != 1:
        print("Virheellinen syöte. Ole hyvä ja syötä 0 rikolliselle tai 1 etsijälle.")
        if role_type == 0:
            print("Valitsit roolin rikolliselle.")
            break
        elif role_type == 1:
            print("Valitsit roolin etsijälle.")
            break
        role_type = int(input("Valitse nyt roolisi. Syötä 0 rikolliselle tai 1 etsijälle: "))

    return role_type


# How many players will be playing the game?
def how_many_players():
    print("Kuinka monta pelaajaa pelaa peliä?\n"
          "Jos vastaus on 1:\n"
          "Pelaaja pelaa tietokonetta vastaan ja pelaajan täytyy valita rooli.\n"
          "Jos vastaus on 2: \n"
          "Ensimmäinen pelaaja pelaa rikollista ja toinen pelaaja pelaa kahta etsijää.\n"
          "Jos vastaus on 3: \n"
          "Ensimmäinen pelaaja pelaa rikollista, toinen pelaaja pelaa etsijää ja kolmas pelaaja pelaa etsijää.")
    try:
        num_players = int(input("Syötä numero 1:n ja 3:n väliltä: "))
        if num_players == 1:
            print("Pelaaja pelaa tietokonetta vastaan.")
            player_choose_the_role()
            return num_players

        elif num_players == 2:
            return num_players
        elif num_players == 3:
            return num_players
        else:
            print("Virheellinen syöte. Syötä numero 1:n ja 3:n väliltä: ")
            how_many_players()
    except ValueError:
        num_players = int(input("Syötä numero 1:n ja 3:n väliltä: "))
    return num_players


def get_players_info(name):
    sql = f"""
        select player.screen_name, player.location, airport.name, country.name 
        from player 
        left join airport on player.location = airport.ident 
        left join country on airport.iso_country = country.iso_country 
        where screen_name = '{name}'
    """
    result = db_query(sql)
    player_info = {}
    if result:
        player_info["screen_name"] = result[0][0]
        player_info["location"] = result[0][1]
        player_info["airport_name"] = result[0][2]
        player_info["country_name"] = result[0][3]
    return player_info


def screen_names():
    sql = "select screen_name from player"
    result = db_query(sql)
    names = []
    for row in result:
        names.append(row[0])
    return names


#Funktio kysyy pelaajan nimeä, tarkistaa onko se tyhjä, liian pitkä
#tai käytössä. Palauttaa hyväksytyn nimimerkin.

def new_player():
    names = screen_names()
    max_char = 20
    while True:
        name = input("Syötä nimimerkki: ")
        if name not in names and name and len(name) <= max_char:
            print(f"Nimimerkki {name} lisätty.")
            return name
        elif not name:
            print("Tyhjä nimimerkki. Yritä uudelleen!")
        elif len(name) > max_char:
            print(f"Nimimerkin on oltava enintään {max_char} merkkiä pitkä.")
        elif name in names:
            print("Nimimerkki on varattu. Valitse uusi.")


def insert_player(name, type, location):
    sql = f"""insert into player (screen_name, type, location) 
    values ('{name}', '{type}', '{location}')"""
    add = db_insert(sql)
    return add


def add_player_game(player_id, game_id):
    sql = f"""insert into player_game (game_id,player_id) 
    values ('{game_id}', '{player_id}')"""
    add = db_insert(sql)


def get_criminal_info(name):
    sql = f"""
        SELECT player.screen_name, player.location, airport.name, country.name, airport.latitude_deg, airport.longitude_deg
        FROM player
        LEFT JOIN airport ON player.location = airport.ident
        LEFT JOIN country ON airport.iso_country = country.iso_country
        WHERE screen_name = '{name}'
    """
    result = db_query(sql)
    criminal_info = {}
    if result:
        criminal_info["screen_name"] = result[0][0]
        criminal_info["location"] = result[0][1]
        criminal_info["airport_name"] = result[0][2]
        criminal_info["country_name"] = result[0][3]
        criminal_info["latitude"] = result[0][4]
        criminal_info["longitude"] = result[0][5]
    return criminal_info
