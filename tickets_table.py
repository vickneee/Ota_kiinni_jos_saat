#Lipun poistaminen
from db_functions import db_delete


def delete_ticket(ticket_type, player_id):
    sql = f"DELETE FROM tickets WHERE ticket_type = '{ticket_type}', '{player_id}'"
    delete = db_delete(sql)
    return delete