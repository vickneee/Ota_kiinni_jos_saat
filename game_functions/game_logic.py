from game_functions.player_move import player_move
from game_functions.ai_move import ai_criminal_move, ai_detective_move
from game_functions.player_management import new_player, insert_player, insert_player_tickets, get_players_info, criminal_choose_starting_point
from game_functions.airport_table import two_farthest_airport
from termcolor import colored


# Player 1, choose your role: (0 or 1)
def player_choose_the_role():
    player_ids = []
    role_type = int(input(colored("Valitse roolisi. Syötä 0 rikolliselle tai 1 etsijällä: ", "green")))
    while role_type != 0 and role_type != 1:
        print(colored("Virheellinen syöte. Ole hyvä ja syötä 0 rikolliselle tai 1 etsijälle.", "red"))
        role_type = int(input(colored("Valitse nyt roolisi. Syötä 0 rikolliselle tai 1 etsijälle: ", "green")))

    if role_type == 0:
        print("Valitsit roolin rikolliselle.")
        setup_players(player_ids, criminal_is_computer=False, detectives_are_computer=True)

    elif role_type == 1:
        print("Valitsit roolin etsijälle.")
        print("Anna ensin vastustajasi (tietokoneen) nimi")
        setup_players(player_ids, criminal_is_computer=True, detectives_are_computer=False)

    return player_ids


# How many players will be playing the game?
def how_many_players():
    player_ids = []
    print("Kuinka monta pelaajaa pelaa peliä?\n"
          "Jos vastaus on 1:\n"
          "Pelaaja pelaa tietokonetta vastaan ja pelaajan täytyy valita rooli.\n"
          "Jos vastaus on 2: \n"
          "Ensimmäinen pelaaja pelaa rikollista ja toinen pelaaja pelaa kahta etsijää.\n"
          "Jos vastaus on 3: \n"
          "Ensimmäinen pelaaja pelaa rikollista, toinen pelaaja pelaa etsijää ja kolmas pelaaja pelaa etsijää.")
    while True:
        try:
            num_players = int(input(colored("Syötä numero 1:n ja 3:n väliltä: ", "green")))
            if num_players == 1:
                print("Pelaaja pelaa tietokonetta vastaan.")
                player_ids = player_choose_the_role()
                return player_ids

            elif num_players == 2 or num_players == 3:
                setup_players(player_ids, criminal_is_computer=False, detectives_are_computer=False)
                return player_ids
            else:
                print(colored("Virheellinen syöte. Syötä numero 1:n ja 3:n väliltä: ", "red"))

        except ValueError:
            print(colored("Virheellinen syöte. Syötä numero 1:n ja 3:n väliltä: ", "red"))


# Create a new player for the criminal
def setup_players(player_ids, criminal_is_computer, detectives_are_computer):
    criminal = new_player(0)
    criminal_id = criminal_choose_starting_point(criminal, criminal_is_computer)
    player_ids.append(criminal_id)

    # Find the two farthest airports for detectives
    farthest = two_farthest_airport(criminal)

    # Create and insert the first detective
    detective1 = new_player(1)
    detective1_id = insert_player(detective1, 1, farthest[0][0], detectives_are_computer)
    insert_player_tickets(detective1_id, 1)
    player_ids.append(detective1_id)

    # Create and insert the second detective
    detective2 = new_player(1)
    detective2_id = insert_player(detective2, 1, farthest[1][0], detectives_are_computer)
    insert_player_tickets(detective2_id, 1)
    player_ids.append(detective2_id)


# Game player round function
def game_player_round(player, round, ids, game_id, screen_names):
    # Get player information
    player = player_info = get_players_info(player)
    if player_info.get('is_computer') == 1:
        if player_info.get('type') == 0:
            # Computer move for criminal
            ai_criminal_move(player.get('screen_name'), game_id)
        else:
            ai_detective_move(screen_names[0], player.get('screen_name'))
    else:
        # Human player move
        player_move(player.get('screen_name'), round, ids, screen_names)
