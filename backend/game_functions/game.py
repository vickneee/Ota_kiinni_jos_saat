from backend.game_functions.player import Player
from backend.game_functions.human_player import HumanPlayer
from backend.game_functions.ai_player import AIPlayer
from backend.game_functions.database import Database


class Game:

    def __init__(self):
        self.database = Database()
        self.game_id = self.create_game()
        self.players = []
        self.screen_names = []
        self.round = 0

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
            SET player_id={player_id},
            date = NOW()
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
        self.round = 1

    def play_round(self,player_name,new_location, ticket_id):
        name_index = self.screen_names.index(player_name)
        other_loc = []
        player = self.players[name_index]
        criminal = ""

        for p in self.players:
            if p.type == 0:
                criminal = p.location
            if p != player:
                other_loc.append(p.location)

        if name_index == 2:
            self.insert_round()
        if player.is_computer == 0:
            player.player_move(new_location, ticket_id)
            self.update_round_player(player.id)
        elif player.is_computer == 1:
           if player.type == 0:
               player.criminal_move(player.location,other_loc)
               self.update_round_player(player.id)
           else:
               player.detective_move(player.location, criminal, self.round)
               self.update_round_player(player.id)
        return




    #Method to fetch all games from DB
    def fetch_saved_games(self):
        try:
            sql = """
                SELECT 
                    game.id AS game_id, 
                    game.round,
                    GROUP_CONCAT(player.screen_name) AS players,
                    game.date
                FROM 
                    game
                LEFT JOIN 
                    game_player ON game.id = game_player.game_id
                LEFT JOIN 
                    player ON game_player.player_id = player.id
                GROUP BY 
                    game.id, game.round, game.date;
            """
            result = self.database.db_query(sql)

            if result:
                # Transform database results into a list of dictionaries
                saved_games = [
                    {
                        "game_id": row[0],
                        "round": row[1],
                        "players": row[2].split(",") if row[2] else [],
                        "date": row[3]  # Include the date field
                    }
                    for row in result
                ]
                return saved_games
            return []

        except Exception as e:
            raise Exception(f"Error fetching saved games: {str(e)}")

