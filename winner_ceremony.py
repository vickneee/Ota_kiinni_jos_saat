import game_over
from db_functions import db_query

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
        return winners, location