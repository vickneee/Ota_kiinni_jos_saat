from game_over import game_over
from db_functions import db_query
from playsound import playsound

# Soitetaan musiikkia kun peli päättyy
def play_celebration_sound():
    playsound('assets/celebration.mp3')

def winner_ceremony():
    if game_over():
    # Haetaan tietokannasta pelaajien nimet ja lokaatio
    # Lokaation avulla voidaan selventää pelin päättyessä missä rikollinen lopulta jäi kiinni
        sql = """
            select screen_name, location
            from player
            where type = 0 or type = 1
            """
        result = db_query(sql)
        winners = ", ".join([row[0] for row in result])
        location = result[0][1]
        play_celebration_sound()
        return winners, location

