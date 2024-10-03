from game import game_id
from game_over import game_over
from db_functions import db_query
from playsound import playsound

# Soitetaan musiikkia kun peli päättyy
def play_celebration_sound():
    playsound('assets/celebration.mp3')

def winner_ceremony(game_id, criminal_id, detective_id):
    if game_over(game_id, criminal_id, detective_id):
    # Haetaan tietokannasta pelaajien nimet ja lokaatio
    # Lokaation avulla voidaan selventää pelin päättyessä missä rikollinen lopulta jäi kiinni
        sql = """
            SELECT p.screen_name, a.name AS location
            FROM player p
            LEFT JOIN game_player gp ON p.id = gp.player_id
            LEFT JOIN airport a ON p.location = a.ident
            WHERE gp.game_id = {game_id} 
            AND (p.id = {criminal_id} OR p.id = {detective_id})
        """
        result = db_query(sql)

        # Voittajien nimet
        winners = [row[0] for row in result]
        criminal_location = None

        # Rikollisen sijainti, koska rikollisen sijainti voidaan näyttää pelin lopussa aina
        for row in result:
            if row[0] == criminal_id:
                criminal_location = row[1]

        play_celebration_sound()

        # Palautetaan aina rikollisen sijainti
        # Palautetaan voittajien nimet
        return ", ".join(winners), criminal_location

    #Alkuperäinen, palauttaa vain ensimmäisen tuloksen lokaation
    # Vaikka pitäisi palauttaa sen lokaation jossa kiinni ottanut etsivä ja kiinni jäänyt roisto sijaitsee
    """result = db_query(sql)
        winners = ", ".join([row[0] for row in result])
        location = result[0][1]
        play_celebration_sound()
        return winners, location
    """

