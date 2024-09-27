from db_functions import db_query, db_insert

# Player 1, choose your role: (0 or 1)
def player_choose_the_role():
    try:
        role_type = int(input("Valitse nyt roolisi. Syötä 0 rikolliselle tai 1 etsijälle: "))
        if role_type == 0:
            print("Olet valinnut rikollisen.")
            return role_type
        elif role_type == 1:
            print("Olet valinnut etsijän.")
            return role_type
        else:
            print("Virheellinen syöte. Ole hyvä ja syötä 0 rikolliselle tai 1 etsijälle.")
            role_type = int(input("Valitse nyt roolisi. Syötä 0 rikolliselle tai 1 etsijälle: "))
    except ValueError:
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


how_many_players()

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

#Funktio kysyy pelaajan nimeä, tarkistaa onko se tyhjä, liian pitkä
#tai käytössä. Palauttaa hyväksytyn nimimerkin.

def new_player(screen_name):
    max_char = 20
    while True:
        name = input("Syötä nimimerkki: ")
        if not name:
            print("Tyhjä nimimerkki. Yritä uudelleen!")
        elif len(name) > max_char:
            print(f"Nimimerkin on oltava enintään {max_char} merkkiä pitkä.")
        elif name in names:
            print("Nimimerkki on varattu. Valitse uusi.")
        else:
            return name

def insert_player(name, type, location):
    sql = f"""insert into player (screen_name, type, location) 
    values ('{name}', '{type}', '{location}')"""
    add = db_insert(sql)
    return add

