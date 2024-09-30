from db_functions import db_insert

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

def start_game():
    game_id = create_game()




