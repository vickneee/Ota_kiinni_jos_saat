from db_functions import db_query

# Check if criminal and detective are in the same location.
# Query checks if type 0 i.e. criminal has the same value in location column
# And type 1 i.e. detective has the same value in location column
def game_over(game_id,criminal_id,detective_id):
    sql_criminal = f"""
            SELECT p.location
            FROM player p
            LEFT JOIN game_player gp ON p.id = gp.player_id
            LEFT JOIN game g ON gp.game_id = g.id
            WHERE p.id='{criminal_id}' AND gp.game_id = {game_id}
        """
    criminal_location = db_query(sql_criminal)
    sql_detective = f"""
            SELECT p.location
            FROM player p
            LEFT JOIN game_player gp ON p.id = gp.player_id
            LEFT JOIN game g ON gp.game_id = g.id
            WHERE p.id='{detective_id}' AND gp.game_id = {game_id}
        """
    detective_location = db_query(sql_detective)

    # Return True if criminal and detective are in the same location
    if criminal_location == detective_location:
        return True
    else:
        return False

#print(game_over(1,1,2)) # True



