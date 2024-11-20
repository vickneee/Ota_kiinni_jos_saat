from backend.game_functions.db_functions import db_query


# Function to retrieve the winner of the game
def winner_ceremony(game_id):
    # Retrieve players and their information from the database for the completed game
    # The location helps clarify where the criminal was finally caught at the end of the game
    # Or from where they flew to freedom after ten rounds
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
