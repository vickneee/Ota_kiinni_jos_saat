from db_functions import db_delete,db_insert


# Lipun poistaminen
def delete_ticket(ticket_type, player_id):
    sql = f"""DELETE FROM tickets 
    WHERE ticket_type = '{ticket_type}' and player_id = '{player_id}' ORDER BY rowid DESC LIMIT 1"""
    delete = db_delete(sql)
    return delete

def insert_tickets(player_id, ticket_type):
    sql = f"""INSERT INTO tickets (player_id, ticket_type) 
    VALUES ('{player_id}', '{ticket_type}')"""
    db_insert(sql)
