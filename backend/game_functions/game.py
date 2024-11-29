from backend.game_functions.ai_player import AIPlayer
#from player import Player
from backend.game_functions.human_player import HumanPlayer
#from ai_player import AIPlayer
from backend.game_functions.database import Database


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

    def insert_round(self):
        sql = f"""
            UPDATE game
            SET round = round +1
            WHERE id = {self.game_id}
        """
        Database().db_update(sql)

    # Update the player_id column in the game table
    def update_round_player(self,player_id):
        sql = f"""
            UPDATE game 
            SET player_id={player_id}
            WHERE id={self.game_id}
        """
        Database().db_update(sql)

    # Add players to the game based on the user input provided by frontend
    # Parameters:
    # payer_data: list of dict, where each dict contains: "name", "player_type"(0 = criminal, 1 = detective), "is_human"(boolean)
    def add_players(self, player_data):

        for pdata in player_data:
            if pdata["is_computer"] == 0:
                player = HumanPlayer(name=pdata["name"], player_type=pdata["player_type"], location=pdata["location"])
            else:
                player = AIPlayer(name=pdata["name"], player_type=pdata["player_type"], location=pdata["location"])

            player.insert_player()
            player.insert_player_tickets()
            player.add_player_to_game(self.game_id)
            self.screen_names.append(pdata["name"])
            self.players.append(player)

    def play_round(self,player_name,new_location, ticket_id):
        name_index = self.screen_names[player_name]
        player = self.players[name_index]
        if isinstance(player, HumanPlayer):
            player.player_move(new_location, ticket_id)
        else:
            pass

