from backend.game_functions.player import Player
from backend.game_functions.human_player import HumanPlayer
from backend.game_functions.ai_player import AIPlayer
from backend.game_functions.database import Database


class Game:

    def __init__(self, game_id=None):
        self.database = Database()
        self.game_id = None
        self.players = []
        self.screen_names = []
        self.round = 0

    #Create a new game in the database and return the game ID
    def create_game_id(self):

        sql_insert = "INSERT INTO game (round, player_id) VALUES (0, null)"
        id = self.database.db_insert(sql_insert)  # Palauttaa uuden pelin ID:n
        print(id)
        self.game_id = id


    def set_game_id(self, game_id):
        self.game_id = game_id

    def reset_game(self):
        self.game_id = None
        self.players = []
        self.round = 0




    def insert_round(self):
        sql = f"""
            UPDATE game
            SET round = round +1
            WHERE id = {self.game_id}
        """
        Database().db_update(sql)
##j
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
        self.insert_round()

    def resume_game(self,data):
        gamedata = data['gamedata'][0]
        self.set_game_id(gamedata['game_id'])
        player_ids = gamedata['playerids']
        self.players = Player.get_players_by_ids(player_ids)
        self.screen_names = [player['screen_name'] for player in self.players]
        self.round = gamedata['round']


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


    #Method to fetch all games from DB
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



# g = Game()
# g.create_game_id()
# pl = {"name": "oia", "player_type": 0, "is_computer": 0, 'location':'EFHK'},{"name": "sad", "player_type": 1, "is_computer": 0,'location':'ESSA'},{"name": "olom", "player_type": 1, "is_computer": 0,'location':'UKBB'}
# g.add_players(pl)
# g.play_round('sad','LIRF',3)
# print(g.players[2].location)

