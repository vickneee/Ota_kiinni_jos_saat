from player_move import player_move
from ai_move import ai_criminal_move, ai_detective_move
from player_management import new_player, insert_player,insert_player_tickets, get_players_info, screen_names,criminal_choose_starting_point
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
    while True:
        try:
            num_players = int(input("Syötä numero 1:n ja 3:n väliltä: "))
            if num_players == 1:
                print("Pelaaja pelaa tietokonetta vastaan.")
                player_ids = player_choose_the_role()
                return player_ids

            elif num_players == 2 or num_players == 3:
                setup_players(player_ids, criminal_is_computer=False, detectives_are_computer=False)
                return player_ids
            else:
                print("Virheellinen syöte. Syötä numero 1:n ja 3:n väliltä: ")

        except ValueError:
            print("Virheellinen syöte. Syötä numero 1:n ja 3:n väliltä: ")




def setup_players(player_ids, criminal_is_computer,detectives_are_computer):
    criminal = new_player(0)
    criminal_id = criminal_choose_starting_point(criminal, criminal_is_computer)
    player_ids.append(criminal_id)
    farthest = two_farthest_airport(criminal)
    detective1 = new_player(1)
    detective1_id = insert_player(detective1, 1, farthest[0][0], detectives_are_computer)
    insert_player_tickets(detective1_id, 1)
    player_ids.append(detective1_id)
    detective2 = new_player(1)
    detective2_id = insert_player(detective2, 1, farthest[1][0], detectives_are_computer)
    insert_player_tickets(detective2_id, 1)
    player_ids.append(detective2_id)


def game_player_round(player, round,ids,game_id,screen_names):

    player = player_info = get_players_info(player)
    if player_info.get('is_computer') == 1:
        if player_info.get('type') == 0:
            ai_criminal_move(player.get('screen_name'),game_id)
        else:
            ai_detective_move(screen_names[0], player.get('screen_name'))
    else:
        player_move(player.get('screen_name'),round,ids,screen_names)





