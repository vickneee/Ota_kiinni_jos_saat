from db_functions import db_insert


def add_player_past_movement(ticket_type, player_id, location):
    sql = f"""insert into past_movement (ticket_type, player_id,location) 
    values ('{ticket_type}', '{player_id}', '{location}')"""
    add = db_insert(sql)
    return add
