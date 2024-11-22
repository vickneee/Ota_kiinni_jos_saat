from flask import Flask, jsonify
import os
app = Flask(__name__)


@app.route('/api/env')
def get_env():
    return jsonify({
        'MAP_KEY': os.getenv('MAP_KEY')
    })

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)