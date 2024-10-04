from db_functions import db_query


def winner_ceremony(game_id):
    # Haetaan tietokannasta päättyneen pelin pelaajat ja heidän tiedot
    # Lokaation avulla voidaan selventää pelin päättyessä missä rikollinen lopulta jäi kiinni
    # Tai mistä hän lensi vapauteen kymmenen kierroksen jälkeen

    sql = f"""
            SELECT screen_name, location, country.name, airport.name
            FROM player
            LEFT JOIN AIRPORT on player.location = airport.ident
            LEFT JOIN country on airport.iso_country = country.iso_country
            LEFT JOIN game_player on player.id = game_player.player_id
            LEFT JOIN game on game.id = game_player.game_id
            WHERE game.id = {game_id}
            """

    result = db_query(sql)
    return result

