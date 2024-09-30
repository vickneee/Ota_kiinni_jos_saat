from db_functions import db_insert
from game_logic import how_many_players
from player_management import add_player_game

# Welcome to the game of Catch me if you can!
def welcome():
    print("Tervetuloa Ota kiinni jos saat -peliin!\n"
          "Peli on yksinkertainen peli, jossa rikollinen yrittää välttää etsijöitä.\n"
          "Pelissä on 10 kierrosta, joiden aikana rikollinen yrittää välttää etsijöitä.\n"
          "Etsijät yrittävät löytää rikollisen ennen kuin rikollinen ehtii paeta.\n"
          "Peli on ohi, kun rikollinen on saatu kiinni eli löydetty.\n"
          "(Etsijät voittavat) tai rikollinen pääsee pakoon (Rikollinen voittaa).\n"
          "Onnea peliin!")


welcome()

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

start_game(game_id)





