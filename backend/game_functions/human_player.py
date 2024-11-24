from player import Player

class HumanPlayer(Player):
    def __init__(self, name, player_type, location, database):
        super().__init__(name, player_type, location, database, is_computer=0)

