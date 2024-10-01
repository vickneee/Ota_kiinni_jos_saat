from db_functions import db_query, db_insert
#from criminal_choose_starting_point import criminal_choose_starting_point
#from two_farthest_airport import two_farthest_airport

from player_management import new_player, insert_player, criminal_choose_starting_point
from airport_table import two_farthest_airport


# Player 1, choose your role: (0 or 1)
def player_choose_the_role():
    player_ids=[]
    role_type = int(input("Valitse roolisi. Syötä 0 rikolliselle tai 1 etsijällä: "))
    while role_type != 0 and role_type != 1:
        print("Virheellinen syöte. Ole hyvä ja syötä 0 rikolliselle tai 1 etsijälle.")
        role_type = int(input("Valitse nyt roolisi. Syötä 0 rikolliselle tai 1 etsijälle: "))

    if role_type == 0:
        print("Valitsit roolin rikolliselle.")
        setup_players(player_ids, criminal_is_computer=False, detectives_are_computer=True)

    elif role_type == 1:
        print("Valitsit roolin etsijälle.")
        print("Anna ensin vastustajasi (tietokoneen) nimi")
        setup_players(player_ids, criminal_is_computer=True, detectives_are_computer=False)


    print(player_ids)
    return player_ids


# How many players will be playing the game?
def how_many_players():
    player_ids=[]
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
            ids = player_choose_the_role()
            return ids

        elif num_players == 2:
            setup_players(player_ids, criminal_is_computer=False, detectives_are_computer=False)

        elif num_players == 3:
            setup_players(player_ids, criminal_is_computer=False, detectives_are_computer=False)
        else:
            print("Virheellinen syöte. Syötä numero 1:n ja 3:n väliltä: ")
            how_many_players()
    except ValueError:
        num_players = int(input("Syötä numero 1:n ja 3:n väliltä: "))
    print(player_ids)
    return player_ids

def setup_players(player_ids, criminal_is_computer,detectives_are_computer):
    criminal = new_player(0)
    criminal_id = criminal_choose_starting_point(criminal, criminal_is_computer)
    player_ids.append(criminal_id)
    farthest = two_farthest_airport(criminal)
    detective1 = new_player(1)
    detective1_id = insert_player(detective1, 1, farthest[0][0], detectives_are_computer)
    player_ids.append(detective1_id)
    detective2 = new_player(1)
    detective2_id = insert_player(detective2, 1, farthest[0][0], detectives_are_computer)
    player_ids.append(detective2_id)




