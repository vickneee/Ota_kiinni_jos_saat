from flask import Flask, jsonify, Response, request
from flask_cors import CORS
import os
import json

from backend.game_functions.airport import Airport
from backend.game_functions.game import Game
from dotenv import load_dotenv
from backend.game_functions.tickets import Tickets
from backend.game_functions.player import Player

load_dotenv()
app = Flask(__name__)
CORS(app)
g = Game()


# Get the environment variables
@app.route('/api/env')
def get_env():
    return jsonify({'MAP_KEY': os.getenv('MAP_KEY')})


# Get all the airports
@app.route('/api/airports')
def airport_locations():
    try:
        airport_instance = Airport()
        all = airport_instance.airports_location()
        status = 200
        ans = {'status': status, 'locations': all}
    except Exception as e:
        status = 500
        ans = {'status': status, 'teksti': 'virheellinen pyyntö', 'error': str(e)}
    jsonans = json.dumps(ans)
    return Response(response=jsonans, status=status, mimetype="application/json")


# Start a new game
@app.route('/api/start_game', methods=['POST'])
def start_game():
    try:
        data = request.json
        players = data.get('players')
        criminal_data = data.get('criminal_location')
        criminal_icao = data.get('criminal_icao')
        criminal_loc = {'latitude': criminal_data['latitude'], 'longitude': criminal_data['longitude']}
        det_starts = Airport().two_farthest_airports(criminal_loc)
        all_loc = [criminal_icao, det_starts[0][0], det_starts[1][0]]
        det1_coord = [{'latitude': det_starts[0][3], 'longitude': det_starts[0][4]}]
        det2_coord = [{'latitude': det_starts[1][3], 'longitude': det_starts[1][4]}]
        player_list = []
        for i in range(3):
            player_list.append({'name': players[i]['name'], 'player_type': players[i]['type'], 'location': all_loc[i],
                                'is_computer': players[i]['is_computer']})
        g.reset_game()
        g.create_game_id()
        g.add_players(player_list)

        status = 200
        ans = {'status': status, 'message': 'Game started successfully', 'players': players,
               'detective1_location': det1_coord, 'detective2_location': det2_coord,
               'criminal_location': criminal_data, }
    except Exception as e:
        import traceback
        error_message = traceback.format_exc()
        print("Error in /api/saved-games:", error_message)
        return jsonify({"status": "error", "message": str(e)}), 500

    jsonans = json.dumps(ans)
    return Response(response=jsonans, status=status, mimetype="application/json")


# Start a new game with AI
@app.route('/api/start_game_ai', methods=['POST'])
def start_game_ai():
    try:
        data = request.json
        players = data.get('players')
        criminal_start = Player.criminal_starting_point()
        criminal_icao = criminal_start[0]
        criminal_coord = {'latitude': criminal_start[1]['latitude'], 'longitude': criminal_start[1]['longitude']}
        det_starts = Airport().two_farthest_airports(criminal_coord)
        all_loc = [criminal_icao, det_starts[0][0], det_starts[1][0]]
        det1_coord = [{'latitude': det_starts[0][3], 'longitude': det_starts[0][4]}]
        det2_coord = [{'latitude': det_starts[1][3], 'longitude': det_starts[1][4]}]
        player_list = []

        for i in range(3):
            player_list.append({'name': players[i]['name'], 'player_type': players[i]['type'], 'location': all_loc[i],
                                'is_computer': players[i]['is_computer']})
        g.reset_game()
        g.create_game_id()
        g.add_players(player_list)

        status = 200
        ans = {'status': status, 'message': 'Game started successfully', 'players': player_list,
               'detective1_location': det1_coord, 'detective2_location': det2_coord, 'criminal_coord': criminal_coord}
    except Exception as e:
        import traceback
        error_message = traceback.format_exc()
        print("Error in /api/start:", error_message)
        return jsonify({"status": "error", "message": str(e)}), 500

    jsonans = json.dumps(ans)
    return Response(response=jsonans, status=status, mimetype="application/json")


# Error handling for 404
@app.errorhandler(404)
def page_not_found(err):
    ans = {"status": "404", "teksti": "Virheellinen päätepiste"}
    jsonans = json.dumps(ans)
    return Response(response=jsonans, status=404, mimetype="application/json")


# Saved games endpoint
@app.route('/api/saved-games', methods=['GET'])
def fetch_saved_games():
    try:
        # Fetch saved games using the method in game.py
        saved_games = g.fetch_saved_games()

        return jsonify({"status": "success", "saved_games": saved_games}), 200

    except Exception as e:
        import traceback
        error_message = traceback.format_exc()
        print("Error in /api/saved-games:", error_message)
        return jsonify({"status": "error", "message": str(e)}), 500


# Get and check if the player exists
@app.route('/api/check-user', methods=['GET'])
def check_player():
    try:
        screen_names = Player.get_screen_names()
        status = 200
        ans = {'status': status, 'player_info': screen_names}

    except Exception as e:
        status = 500
        ans = {'status': status, 'teksti': 'virheellinen pyyntö', 'error': str(e)}
    jsonans = json.dumps(ans)
    return Response(response=jsonans, status=status, mimetype="application/json")


# Get player tickets
@app.route('/api/player-tickets/<int:player_id>', methods=['GET'])
def player_tickets(player_id):
    try:
        tickets = Tickets().player_tickets(player_id)
        return jsonify({"status": "success", "tickets": tickets}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# Ge player round
@app.route('/api/round/<int:game_id>', methods=['GET'])
def get_round(game_id):
    try:
        round = Player.get_round(game_id)
        return jsonify({"status": "success", "round": round}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# Get player screen names
@app.route('/api/game-screen-names/<int:game_id>', methods=['GET'])
def game_screen_names(game_id):
    try:
        screen_names = Player.get_game_screen_names(game_id)
        return jsonify({"status": "success", "screen_names": screen_names}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# Post play round
@app.route('/api/play_round', methods=['POST'])
def play_round():
    try:
        data = request.json
        if not data:
            raise ValueError("No data provided in request.")

        player = data.get('player')
        new_location = data.get('new_location')
        ticket_id = data.get('ticket_id')
        is_computer = data.get('is_computer')
        # Validate input data
        if not player or not new_location or not ticket_id:
            raise ValueError("Missing required fields: 'player', 'new_location', or 'ticket_id'.")

        print(f"Player: {player}, New Location: {new_location}, Ticket ID: {ticket_id}")

        # Perform the move
        move = g.play_round(player, new_location, ticket_id)
        print(move)
        status = 200
        if is_computer == 1:
            coords = Airport().airports_coord(move)
            print()
            ans = {'status': status, 'message': 'Move made successfully', 'icao': move, 'coords': coords}
        else:
            ans = {'status': status, 'message': 'Move made successfully'}

    except Exception as e:
        # Log detailed error
        import traceback
        error_message = traceback.format_exc()
        print("Error in /api/play_round:", error_message)

        # Response for failure
        status = 500
        ans = {'status': status, 'message': 'Failed to make a move', 'error': str(e),
               'details': error_message.splitlines()}

    # Return JSON response
    jsonans = json.dumps(ans)
    return Response(response=jsonans, status=status, mimetype="application/json")


# Get player data
@app.route('/api/getdata', methods=['GET'])
def get_data():
    try:
        game_id = g.game_id
        players = Player.get_game_players(game_id)

        status = 200
        ans = {'status': status, 'game_id': game_id, 'players': players}
    except Exception as e:
        import traceback
        error_message = traceback.format_exc()
        print("Error in /api/getdata:", error_message)
        status = 500
        ans = {'status': status, 'message': 'Failed to retrieve data', 'error': str(e)}

    jsonans = json.dumps(ans)
    return Response(response=jsonans, status=status, mimetype="application/json")


# Resume game
@app.route('/api/resume_game', methods=['PUT'])
def resume_game():
    try:
        data = request.json
        gamedata = data.get('gamedata')

        g.reset_game()
        g.resume_game(gamedata)
        status = 200
        ans = {'status': status, 'gamedata': gamedata, 'id': g.game_id}
    except Exception as e:
        import traceback
        error_message = traceback.format_exc()
        print("Error in /api/getdata:", error_message)
        status = 500
        ans = {'status': status, 'message': 'Failed to retrieve data', 'error': str(e)}

    jsonans = json.dumps(ans)
    return Response(response=jsonans, status=status, mimetype="application/json")


# Get current turn
@app.route('/api/current-turn/<int:game_id>', methods=['GET'])
def get_current_turn(game_id):
    try:
        current_turn = g.get_current_turn(game_id)

        if current_turn:
            return jsonify({"status": "success", "current_player_id": current_turn}), 200
        else:
            return jsonify({"status": "error", "message": "Game not found"}), 404

    except Exception as e:
        import traceback
        error_message = traceback.format_exc()
        print("Error in /api/current-turn:", error_message)
        return jsonify({"status": "error", "message": str(e)}), 500


# Get recommended airports based on the players location and ticket types
@app.route('/api/get-recommended-airports/<name>/<int:round>', methods=['GET'])
def get_recommended_airports(name, round):
    try:
        recommended_airports = Airport().get_recommended_airports(name, round)
        return jsonify({"status": "success", "recommended_airports": recommended_airports}), 200
    except Exception as e:
        import traceback
        error_message = traceback.format_exc()
        print("Error in /api/getdata:", error_message)
        status = 500
        ans = {'status': status, 'message': 'Failed to retrieve data', 'error': str(e)}


# Get criminal movements
@app.route('/api/criminal/<int:id>', methods=['GET'])
def criminal_moves(id):
    try:
        past_location = Player.get_criminal_movements(id)
        return jsonify({"status": "success", "past_location": past_location}), 200
    except Exception as e:
        import traceback
        error_message = traceback.format_exc()
        print("Error in /api/getdata:", error_message)
        status = 500
        ans = {'status': status, 'message': 'Failed to retrieve data', 'error': str(e)}

@app.route('/api/delete_game/<int:id>/<player_ids>', methods=['DELETE'])
def delete_game(id, player_ids):
    try:
        g.delete_game(id, player_ids)
        return jsonify({"status": "success", "message": f"Game with id {id} deleted successfully"}), 200
    except Exception as e:
        import traceback
        error_message = traceback.format_exc()
        print(f"Error in /api/delete_game/{id}:", error_message)
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)
