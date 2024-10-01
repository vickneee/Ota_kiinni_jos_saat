from db_functions import db_delete


# Lipun poistaminen
def delete_ticket(ticket_type, player_id):
    sql = f"""DELETE FROM tickets 
    WHERE ticket_type = '{ticket_type}', '{player_id}' ORDER BY rowid DESC LIMIT 1"""
    delete = db_delete(sql)
    return delete
