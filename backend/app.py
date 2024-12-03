from flask import Flask, jsonify, Response, request
from flask_cors import CORS
import os
import json

from backend.game_functions.database import Database
from backend.game_functions.airport import Airport
from backend.game_functions.game import Game
from dotenv import load_dotenv
from backend.game_functions.tickets import Tickets
from backend.game_functions.player import Player

load_dotenv()
app = Flask(__name__)
CORS(app)
g = Game()

@app.route('/api/env')
def get_env():
    return jsonify({
        'MAP_KEY': os.getenv('MAP_KEY')
    })

@app.route('/api/airports')
def airport_locations():
    try:
        airport_instance = Airport()
        all = airport_instance.airports_location()
        status = 200
        ans = {
            'status': status,
            'locations': all
        }
    except Exception as e:
        status = 500
        ans = {
            'status': status,
            'teksti': 'virheellinen pyyntö',
            'error': str(e)
        }
    jsonans = json.dumps(ans)
    return Response(response=jsonans, status=status, mimetype="application/json")

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
        player_list = []
        for i in range(3):
            player_list.append({'name': players[i]['name'], 'player_type': players[i]['type'], 'location': all_loc[i], 'is_computer': players[i]['is_computer']})

        g.add_players(player_list)

        status = 200
        ans = {
            'status': status,
            'message': 'Game started successfully',
            'players': player_list,
            'all': all_loc
        }
    except Exception as e:
        status = 500
        ans = {
            'status': status,
            'message': 'Failed to start game',
            'error': str(e)
        }

    jsonans = json.dumps(ans)
    return Response(response=jsonans, status=status, mimetype="application/json")

@app.errorhandler(404)
def page_not_found(err):
    ans = {
        "status": "404",
        "teksti": "Virheellinen päätepiste"
    }
    jsonans = json.dumps(ans)
    return Response(response=jsonans, status=404, mimetype="application/json")

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

@app.route('/api/check-user', methods=['GET'])
def check_player():
    try:
        screen_names = Player.get_screen_names()
        status = 200
        ans = {
            'status': status,
            'player_info': screen_names
        }

    except Exception as e:
        status = 500
        ans = {
            'status': status,
            'teksti': 'virheellinen pyyntö',
            'error': str(e)
        }
    jsonans = json.dumps(ans)
    return Response(response=jsonans, status=status, mimetype="application/json")

@app.route('/api/player-tickets/<int:player_id>', methods=['GET'])
def player_tickets(player_id):
    try:
        tickets = Tickets().player_tickets(player_id)
        return jsonify({"status": "success", "tickets": tickets}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/round/<int:game_id>', methods=['GET'])
def get_round():
    try:
        round = Player.get_round(g.game_id)
        return jsonify({"status": "success", "round": round}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/game-screen-names/<int:game_id>', methods=['GET'])
def game_screen_names(game_id):
    try:
        screen_names = Player.get_game_screen_names(game_id)
        return jsonify({"status": "success", "screen_names": screen_names}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/game_players', methods=['GET'])
def game_data():
    try:
        game_id = g.game_id
        players = Player.get_game_players(game_id)

        status = 200
        ans = {
            'status': status,
            'players': players,
            'game_id' : game_id
        }
    except Exception as e:
        status = 500
        ans = {
            'status': status,
            'teksti': 'virheellinen pyyntö',
            'error': str(e)
        }
    jsonans = json.dumps(ans)
    return Response(response=jsonans, status=status, mimetype="application/json")




if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)