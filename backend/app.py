from flask import Flask, Response
import os
app = Flask(__name__)

MAP_KEY = "AIzaSyAjpg5HH9JQ_kRslSMySkifRdCXX3kWYag"


if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)