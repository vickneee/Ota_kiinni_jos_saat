from backend.game_functions.player import Player
from backend.game_functions.human_player import HumanPlayer
from backend.game_functions.ai_player import AIPlayer
from backend.game_functions.database import Database


# Class to handle game data
class Game:

    def __init__(self, game_id=None):
        self.database = Database()
        self.game_id = None
        self.players = []
        self.screen_names = []
        self.round = 0

    # Create a new game in the database and return the game ID
    def create_game_id(self):

        sql_insert = "INSERT INTO game (round, player_id) VALUES (0, null)"
        id = self.database.db_insert(sql_insert)  # Palauttaa uuden pelin ID:n
        print(id)
        self.game_id = id

    # Set the game ID
    def set_game_id(self, game_id):
        self.game_id = game_id

    def reset_game(self):
        self.game_id = None
        self.players = []
        self.round = 0
        self.screen_names = []

    # Insert a new round into the game table
    def insert_round(self):
        sql = f"""
            UPDATE game
            SET round = round +1
            WHERE id = {self.game_id}
        """
        Database().db_update(sql)
        self.round = self.round + 1

    # Update the player_id column in the game table
    def update_round_player(self, player_id):
        sql = f"""
            UPDATE game 
            SET player_id={player_id},
            date = NOW()
            WHERE id={self.game_id}
        """
        Database().db_update(sql)

    # Add players to the game based on the user input provided by frontend
    # Parameters:
    # Player_data: list of dict, where each dict contains: "name", "player_type"(0 = criminal, 1 = detective),
    # "is_human"(boolean)
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
        self.insert_round()

    # Method to resume a game
    def resume_game(self, data):
        gamedata = data
        self.set_game_id(gamedata['game_id'])
        player_ids = gamedata['playerids'].split(',')
        player_ids_str = ','.join(player_ids)
        players = Player.get_players_by_ids(player_ids_str)
        print(players)
        for p in players:
            if p['is_computer'] == 1:
                player = AIPlayer(p['screen_name'], p['type'], p['location'])
            else:
                player = HumanPlayer(p['screen_name'], p['type'], p['location'])

            player.id = p['id']
            self.players.append(player)
            self.screen_names.append(p['screen_name'])

        self.round = gamedata['round']

    # Play a round of the game and return the new location of the player
    def play_round(self, player_name, new_location, ticket_id):
        # Find the index of the player
        if player_name not in self.screen_names:
            raise ValueError(f"Player name '{player_name}' not found in screen names: {self.screen_names}")
        name_index = self.screen_names.index(player_name)
        other_loc = []
        player = self.players[name_index]
        criminal = ""
        other_ai_loc = ""

        # Gather criminal location and other player locations
        for p in self.players:
            if p.type == 0:
                criminal = p.id
            if p != player:
                other_loc.append(p.location)
                if p.is_computer == 1:
                    other_ai_loc = p.location
                else:
                    other_ai_loc = ""

        # Handle round insertion if necessary
        if name_index == 2 and self.round < 11:
            self.insert_round()

        # Process player moves
        if player.is_computer == 0:
            player.player_move(new_location, ticket_id)
            self.update_round_player(player.id)
        elif player.is_computer == 1:
            if player.type == 0:
                aicriminal = player.criminal_move(player.location, other_loc)
                self.update_round_player(player.id)
                return aicriminal
            else:
                aidetective = player.detective_move(player.location, criminal, self.round, other_ai_loc)
                self.update_round_player(player.id)
                return aidetective

        return

    # Method to get player id whose turn it is
    def get_current_turn(self, game_id):
        sql = f"""
            SELECT player_id
            FROM game
            WHERE id = {game_id}
        """
        result = self.database.db_query(sql)
        if result:
            return result[0][0]
        return None

    # Method to fetch all games from DB
    def fetch_saved_games(self):
        try:
            sql = """
                SELECT 
                    game.id AS game_id, 
                    game.round,
                    GROUP_CONCAT(player.screen_name) AS players,
                    GROUP_CONCAT(player.id) AS playerids,
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
                        "playerids": row[3],
                        "date": row[4]
                    }
                    for row in result
                ]
                return saved_games
            return []

        except Exception as e:
            raise Exception(f"Error fetching saved games: {str(e)}")

    def delete_game(self, game_id, player_ids):
        try:
            self.database.db_begin_transaction()
            sql1 = f"DELETE FROM player_tickets WHERE player_id IN (SELECT player_id FROM game_player WHERE game_id = {game_id});"
            self.database.db_update(sql1)

            sql2 = f"DELETE FROM past_movement WHERE player_id IN (SELECT player_id FROM game_player WHERE game_id = {game_id});"
            self.database.db_update(sql2)

            sql3 = f"DELETE FROM game WHERE id = {game_id};"
            self.database.db_update(sql3)

            sql4 = f"DELETE FROM game_player WHERE game_id = {game_id};"
            self.database.db_update(sql4)

            sql5 = f"DELETE FROM player WHERE id IN ({player_ids});"
            self.database.db_update(sql5)

            self.database.db_commit_transaction()
        except Exception as e:
            self.database.db_rollback_transaction()
            print(f"Error deleting game!!!! gameid: {game_id}: {e}")
