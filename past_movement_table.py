from db_functions import db_insert, db_query
from tickets_table import delete_ticket


def add_player_past_movement(ticket_type, player_id, location):
    # Get the last ticket information of the player
    sql = "SELECT ticket_type, player_id FROM tickets ORDER BY rowid DESC LIMIT 1"
    result = db_query(sql)
    if not result:
        return False

    # Add the ticket and player information to the database
    sql = f"""INSERT INTO past_movement (ticket_type, player_id, location) 
              VALUES ('{ticket_type}', '{player_id}', '{location}')"""
    add = db_insert(sql)

    # After that delete the ticket from the tickets table
    result = delete_ticket(ticket_type, player_id)
    if not result:
        return False

    return add
