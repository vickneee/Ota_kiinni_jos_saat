from player import Player

class Ai_player(Player):
    def __iniit__(self, name, player_type, location, database):
        super().__init__(name, player_type, location, database, is_computer=1)

