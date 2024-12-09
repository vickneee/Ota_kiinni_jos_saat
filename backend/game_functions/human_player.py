from backend.game_functions.airport import Airport
from backend.game_functions.player import Player
from backend.game_functions.tickets import Tickets


# Class to handle human player data
class HumanPlayer(Player):
    def __init__(self, name, player_type, location):
        super().__init__(name, player_type, location)

    # Player movement method
    def player_move(self, new_location, ticket_id):

        if self.type == 0:
            self.add_player_past_movement(self.location, ticket_id,self.id )
            self.update_location(new_location)
            self.location = new_location

        else:
            self.update_location(new_location)
            self.location = new_location
            Tickets().delete_ticket(ticket_id, self.id)
