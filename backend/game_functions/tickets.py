from backend.game_functions.database import Database

class Tickets:
    def __init__(self):
        pass
    # Method to delete a ticket from the tickets table
    def delete_ticket(self,ticket_id, player_id):
        sql = f"""DELETE FROM player_tickets 
            WHERE ticket_id = '{ticket_id}' AND player_id='{player_id}'  LIMIT 1"""
        delete = Database().db_delete(sql)
        return delete


    # Method to insert tickets into the tickets table
    def insert_tickets(self,player_id, ticket_id):
        sql = f"""INSERT INTO player_tickets (player_id, ticket_id) 
            VALUES ('{player_id}', '{ticket_id}')"""
        Database().db_insert(sql)


    # Method to get player tickets from the tickets table
    def player_tickets(self,player_id):
        sql = f"""SELECT ticket.type, count(*) 
            FROM ticket left join player_tickets on ticket.id = player_tickets.ticket_id
            WHERE player_id = '{player_id}'
            group by ticket.type"""

        result = Database().db_query(sql)
        tickets = {}
        for row in result:
            tickets[row[0]] = row[1]
        return tickets


print(Tickets().player_tickets(15))


