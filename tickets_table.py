from db_functions import db_delete,db_insert,db_query


# Lipun poistaminen
def delete_ticket(ticket_type, player_id):
    sql = f"""DELETE FROM tickets 
    WHERE ticket_type = '{ticket_type}' and  player_id = '{player_id}' LIMIT 1"""
    delete = db_delete(sql)
    return delete

def insert_tickets(player_id, ticket_type):
    sql = f"""INSERT INTO tickets (player_id, ticket_type) 
    VALUES ('{player_id}', '{ticket_type}')"""
    db_insert(sql)

def player_tickets(player_id):
    sql = f"""SELECT ticket_type, count(*)FROM tickets 
    WHERE player_id = '{player_id}'
    group by ticket_type"""
    result = db_query(sql)
    tickets = {}
    for row in result:
        tickets[row[0]] = row[1]
    return tickets



