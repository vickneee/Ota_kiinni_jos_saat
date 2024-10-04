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
            SELECT screen_name, location
            FROM player
            LEFT JOIN game_player on player.id = game_player.player_id
            WHERE game_player.game_id = {game_id}
            """

        result = db_query(sql)
        """
        # Voittajien nimet
        winners = [row[0] for row in result]
        criminal_location = None

        # Rikollisen sijainti, koska rikollisen sijainti voidaan näyttää pelin lopussa aina
        for row in result:
            if row[0] == criminal_id:
                criminal_location = row[1]
        """
        play_celebration_sound()

        # Palautetaan aina rikollisen sijainti
        # Palautetaan voittajien nimet
        # Palautetaan rikollisen sijainti

        #return ", ".join(winners), criminal_location
        return result


    #Alkuperäinen, palauttaa vain ensimmäisen tuloksen lokaation
    # Vaikka pitäisi palauttaa sen lokaation jossa kiinni ottanut etsivä ja kiinni jäänyt roisto sijaitsee
    """result = db_query(sql)
        winners = ", ".join([row[0] for row in result])
        location = result[0][1]
        play_celebration_sound()
        return winners, location
    """


