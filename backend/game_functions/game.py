from backend.game_functions.ai_player import AIPlayer
from player import Player
from human_player import HumanPlayer
from ai_player import AIPlayer
from database import Database


class Game:

    def __init__(self):
        self.database = Database()
        self.game_id = self.create_game()
        self.players = []
        self.screen_names = []

    #Create a new game in the database and return the game ID
    def create_game(self):

        sql = "INSERT INTO game (round, player_id) VALUES (0, null)"
        return self.database.db_insert(sql)  # Palauttaa uuden pelin ID:n

    # Add players to the game based on the user input provided by frontend
    # Parameters:
    # payer_data: list of dict, where each dict contains: "name", "player_type"(0 = criminal, 1 = detective), "is_human"(boolean)
    def add_players(self, player_data):

        for pdata in player_data:

            if pdata["is_human"]:
                player = HumanPlayer(name=pdata["name"], player_type=pdata["player_type"], location=None,
                                     database=self.database)
            else:
                player = AIPlayer(name=pdata["name"], player_type=pdata["player_type"], location=None,
                                  database=self.database)


            player.insert_player()
            player.add_player_to_game(self.game_id)
            self.players.append(player)


