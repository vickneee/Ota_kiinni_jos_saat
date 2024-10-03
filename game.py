from db_functions import db_insert
from game_logic import how_many_players, game_player_round
from game_over import game_over
from player_management import add_player_game
from insert_rounds import insert_round, update_round_player

# Welcome to the game of Catch me if you can!
def welcome():
    print("Tervetuloa Ota kiinni jos saat -peliin!\n"
          "Peli on yksinkertainen peli, jossa rikollinen yrittää välttää etsijöitä.\n"
          "Pelissä on 10 kierrosta, joiden aikana rikollinen yrittää välttää etsijöitä.\n"
          "Etsijät yrittävät löytää rikollisen ennen kuin rikollinen ehtii paeta.\n"
          "Peli on ohi, kun rikollinen on saatu kiinni eli löydetty.\n"
          "(Etsijät voittavat) tai rikollinen pääsee pakoon (Rikollinen voittaa).\n"
          "Onnea peliin!")
    return

def create_game():
    sql = "INSERT INTO game () VALUES ()"
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
    welcome()
    ids = start_game(game_id)

    screen_names = all_game_screen_names(game_id)


    for round in range(10):

        round += 1
        insert_round(game_id)
        for player in screen_names:
            player_info = get_players_info(player)
            print(f"Pelaaja: {player_info.get('screen_name')}")
            player_id = player_info.get('id')
            game_player_round(player, round, ids, game_id, screen_names)
            update_round_player(player_id, game_id)
            if player_info.get('type') == 1:
                if game_over(game_id, ids[0], player_id):
                    print(game_over(game_id, ids[0], player_id))
                    print("Peli päättyi!")
                    return



game(game_id)









