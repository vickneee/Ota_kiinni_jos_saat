from backend.game_functions.database import db_update, db_query


# Insert a new round into the game table
def insert_round(game_id):
    sql = f"""
        UPDATE game
        SET round = round +1
        WHERE id = {game_id}
    """
    db_update(sql)


# Update the player_id column in the game table
def update_round_player(player_id, game_id):
    sql = f"""
        UPDATE game 
        SET player_id={player_id}
        WHERE id={game_id}
    """
    db_update(sql)


# Get the round from the game table
def get_round(player_id):
    sql = f"""
        SELECT round 
        FROM game 
        LEFT JOIN game_player on game.id = game_player.game_id
        LEFT JOIN player on game_player.player_id = player.id
        WHERE player.id = {player_id}
    """
    result = db_query(sql)
    round = result[0][0]
    return round
