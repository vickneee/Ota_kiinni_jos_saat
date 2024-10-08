from game_functions.db_functions import db_insert
from game_functions.game_logic import how_many_players, game_player_round
from game_functions.game_over import game_over
from game_functions.player_management import add_player_game
from game_functions.insert_rounds import insert_round, update_round_player
from game_functions.assisting_functions import play_celebration_sound, thank_you, welcome


# Create game function
def create_game():
    sql = "INSERT INTO game (round, player_id) VALUES (0, null)"
    game_id = db_insert(sql)
    return game_id


# Create game
game_id = create_game()


# Start game function
def start_game(game_id):
    players = how_many_players()
    for i in range(3):
        player_id = players[i]
        add_player_game(player_id, game_id)
    return players


# Main game function
def game(game_id):
    from game_functions.player_management import all_game_screen_names, get_players_info
    from game_functions.winner_ceremony import winner_ceremony
    welcome()
    ids = start_game(game_id)
    screen_names = all_game_screen_names(game_id)

    # Nested for loops to iterate through the rounds and players
    for round in range(10):
        round += 1
        insert_round(game_id)
        for player in screen_names:
            player_info = get_players_info(player)
            player_id = player_info.get('id')
            if player_info.get('type') == 1:
                if game_over(game_id, ids):
                    print(f"Rikollinen on saatu kiinni ja etsivät {screen_names[1]} ja {screen_names[2]} voittavat!")
                    thank_you()
                    play_celebration_sound()
                    return
            player_turn = game_player_round(player, round, ids, game_id, screen_names)
            if player_turn == "x":
                thank_you()
                return
            update_round_player(player_id, game_id)
            # If the player is the detective, check if the game is over

    # The rounds end after 10 rounds
    # That's when the criminal wins!
    # Play music when the game ends
    if round == 10:
        winners = winner_ceremony(game_id)
        print("Kierrokset loppuivat.")
        print(f"Rikollinen {winners[0][0]} pääsi karkuun!")
        print(f"{winners[0][0]} lensi vapauteen lentokentältä {winners[0][3]}, {winners[0][2]}.")
        thank_you()
        play_celebration_sound()


game(game_id)
