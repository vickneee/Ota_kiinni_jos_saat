from game_functions.db_functions import db_update,db_query

# Lisätään yksi kierros round columniin
def insert_round(game_id):
    sql= f"""
        UPDATE game
        SET round = round +1
        where id = {game_id}
    """
    db_update(sql)


# Update the player_id column in the game table
def update_round_player(player_id, game_id):
    sql = f"""
        UPDATE game 
        set player_id={player_id}
        where id={game_id}
    """
    db_update(sql)

def get_round(player_id):
    sql = f"""
        select round from game 
        left join game_player on game.id = game_player.game_id
        left join player on game_player.player_id = player.id
        where player.id = {player_id}
    """
    result = db_query(sql)
    round = result[0][0]
    return round

