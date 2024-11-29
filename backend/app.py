from flask import Flask, jsonify,Response
from flask_cors import CORS

import os
import json
from backend.game_functions.airport import Airport

from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
CORS(app)

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
    #return jsonify(all)

@app.errorhandler(404)
def page_not_found(err):
    ans = {
        "status" : "404",
        "teksti" : "Virheellinen päätepiste"
    }
    jsonans = json.dumps(ans)
    return Response(response=jsonans, status=404, mimetype="application/json")

@app.route('/api/saved-games', methods=['GET'])
def fetch_saved_games():
    try:
        sql = """
        SELECT 
            game.id AS game_id,
            game.round,
            GROUP_CONCAT(player.screen_name) AS players
        FROM 
            game
        LEFT JOIN 
            game_player ON game.id = game_player.game_id
        LEFT JOIN 
            player ON game_player.player_id = player.id
        GROUP BY 
            game.id, game.round;
        """
        result = database.db_query(sql)

        saved_games = []
        if result:
            for row in result:
                saved_games.append({
                    "game_id": row[0],
                    "round": row[1],
                    "players": row[2].split(",") if row[2] else []
                })

        return jsonify({"status": "success", "saved_games": saved_games}), 200

    except Exception as e:
        import traceback
        error_message = traceback.format_exc()
        print("Error in /api/saved-games:", error_message)
        return jsonify({"status": "error", "message": str(e)}), 500






if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)