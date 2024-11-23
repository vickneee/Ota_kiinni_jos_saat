from flask import Flask, jsonify
import os
import json
from backend.game_functions.airport import Airport

app = Flask(__name__)


@app.route('/api/env')
def get_env():
    return jsonify({
        'MAP_KEY': os.getenv('MAP_KEY')
    })

@app.route('/api/airports')
def airport_locations():
    airport_instance = Airport()
    all = airport_instance.airports_location()
    return jsonify(all)


if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)