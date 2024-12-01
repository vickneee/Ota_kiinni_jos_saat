from backend.game_functions.airport import Airport
from backend.game_functions.player import Player
from backend.game_functions.tickets import Tickets
from backend.game_functions.database import Database


class HumanPlayer(Player):
    def __init__(self, name, player_type, location, database):
        super().__init__(name, player_type, location, database)

    def player_move(self, new_location, ticket_id):

        if self.type == 0:
            self.add_player_past_movement(self.id, self.location, ticket_id)
            self.update_location(new_location)

        else:
            self.update_location(new_location)
            Tickets().delete_ticket(ticket_id, self.id)

# t = HumanPlayer('isä',0, 'EFHK')
# t.insert_player()
