from db_functions import db_update


# Add one round to the round column
def insert_round(game_id):
    sql = f"""
        UPDATE game
        SET round = round +1
        where id = {game_id}
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


# Insert a new round
insert_round(1)
