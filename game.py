from db_functions import db_insert
from game_logic import how_many_players, game_player_round
from game_over import game_over
from player_management import add_player_game
from insert_rounds import insert_round, update_round_player
from winner_ceremony import winner_ceremony



# Welcome to the game of Catch me if you can!
def welcome():
    print("Tervetuloa 'Ota kiinni jos saat' -peliin!\n"
          "Tavoitteena on, että rikollinen välttelee etsiviä 10 kierroksen ajan.\n"
          "Etsivät yrittävät löytää rikollisen ennen kierrosten loppua.\n"
          "Peli päättyy, kun rikollinen joko jää kiinni (etsivät voittavat) "
          "tai onnistuu pakenemaan kierrosten loputtua (rikollinen voittaa).\n"
          "\nOnnea peliin!")
    return

def create_game():
    sql = "INSERT INTO game (round,player_id) VALUES (0,null)"
    game_id = db_insert(sql)
    return game_id

game_id = create_game()

def start_game(game_id):
    players = how_many_players()
    for i in range (3):
        player_id = players[i]
        add_player_game(player_id, game_id)
    return players

#start_game(game_id)

# Pelin runko.

def game(game_id):
    from player_management import all_game_screen_names,get_players_info
    from winner_ceremony import winner_ceremony
    welcome()
    ids = start_game(game_id)

    screen_names = all_game_screen_names(game_id)


    for round in range(1):

        round += 1
        insert_round(game_id)
        for player in screen_names:
            player_info = get_players_info(player)
            print(f"Pelaaja: {player_info.get('screen_name')}")
            player_id = player_info.get('id')
            game_player_round(player, round, ids, game_id, screen_names)
            update_round_player(player_id, game_id)
            if player_info.get('type') == 1:

                    #print(game_over(game_id, ids[0], player_id))
                    #winner_ceremony(game_id, ids[0], player_id)
                    return
    if round == 1:
        winners, location = winner_ceremony(game_id, ids[0], ids[1])
        print(f"Voittajat: {winners}")
        print(f"Rikollisen sijainti: {location}")


game(game_id)










