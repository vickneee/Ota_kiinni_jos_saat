from backend.game_functions.db_functions import db_query


# Check if criminal and detective are in the same location.
# Query checks if type 0 i.e. criminal has the same value in location column
# And type 1 i.e. detective has the same value in location column
def game_over(game_id, ids):

    sql_criminal = f"""
            SELECT p.location
            FROM player p
            LEFT JOIN game_player gp ON p.id = gp.player_id
            LEFT JOIN game g ON gp.game_id = g.id
            WHERE p.id={ids[0]} AND gp.game_id = {game_id}
   """
    criminal_location = db_query(sql_criminal)

    sql_detectives = f"""
            SELECT p.location
            FROM player p
            LEFT JOIN game_player gp ON p.id = gp.player_id
            LEFT JOIN game g ON gp.game_id = g.id
            WHERE p.id in ({ids[1]}, {ids[2]})AND gp.game_id = {game_id}
    """
    detectives_location = db_query(sql_detectives)

    # Return True if criminal and detective are in the same location
    if criminal_location[0] == detectives_location[0] or criminal_location[0] == detectives_location[1]:
        return True
    else:
        return False

