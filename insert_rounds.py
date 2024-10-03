from db_functions import db_update

# Lisätään yksi kierros round columniin
def insert_round(game_id):
    sql= f"""
        UPDATE game
        SET round = round +1
        where id = '{game_id}'
        """
    db_update(sql)


def update_round_player(player_id,game_id):
    sql = f"""
        UPDATE game 
        set player_id={player_id}
        where id={game_id}
    """
    db_update(sql)