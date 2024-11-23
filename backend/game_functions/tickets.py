from backend.game_functions.database import Database

class Tickets:
    # Method to delete a ticket from the tickets table
    def delete_ticket(self,ticket_type, player_id):
        sql = f"""DELETE FROM tickets 
            WHERE ticket_type = '{ticket_type}' AND player_id='{player_id}'  LIMIT 1"""
        delete = Database().db_delete(sql)
        return delete


    # Method to insert tickets into the tickets table
    def insert_tickets(self,player_id, ticket_type):
        sql = f"""INSERT INTO tickets (player_id, ticket_type) 
            VALUES ('{player_id}', '{ticket_type}')"""
        Database().db_insert(sql)


    # Method to get player tickets from the tickets table
    def player_tickets(self,player_id):
        sql = f"""SELECT ticket_type, count(*) 
            FROM tickets 
            WHERE player_id = '{player_id}'
            group by ticket_type"""
        result = Database().db_query(sql)
        tickets = {}
        for row in result:
            tickets[row[0]] = row[1]
        return tickets



