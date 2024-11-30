from flask import Flask, jsonify,Response,request
from flask_cors import CORS
import os
import json
from backend.game_functions.airport import Airport
from backend.game_functions.game import Game
from dotenv import load_dotenv
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
        ans={
            'status':status,
            'locations':all
        }
    except Exception as e:
        status = 500
        ans = {
            'status': status,
            'teksti':'virheellinen pyyntö',
            'error':str(e)
        }
    jsonans = json.dumps(ans)
    return Response(response=jsonans, status=status, mimetype="application/json")

@app.route('/api/start_game',methods = ['POST'])
def start_game():
    try:
        data = request.json
        players = data.get('players')
        criminal_data = data.get('criminal_location')
        criminal_icao = data.get('criminal_icao')
        criminal_loc = {'latitude':criminal_data['latitude'],'longitude':criminal_data['longitude']}
        det_starts = Airport().two_farthest_airports(criminal_loc)
        all_loc = [criminal_icao, det_starts[0][0], det_starts[1][0]]
        player_list = []
        for i in range(3):
            player_list.append({'name':players[i]['name'], 'player_type':players[i]['type'],'location':all_loc[i],'is_computer':players[i]['is_computer']})

        g.add_players(player_list)

        status = 200
        ans = {
            'status': status,
            'message': 'Game started successfully',
            'players': player_list,

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
        "status" : "404",
        "teksti" : "Virheellinen päätepiste"
    }
    jsonans = json.dumps(ans)
    return Response(response=jsonans, status=404, mimetype="application/json")

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)