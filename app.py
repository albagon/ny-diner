import os
from flask import Flask, redirect, url_for
from flask_cors import CORS
from models import setup_db

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    # Allow CORS for all domains on all routes
    CORS(app)

    @app.route('/')
    def index():
        healthy = os.environ['HEALTHY']
        if healthy == 'true': print("Super healthy!")
        return "Good progress!!"

    @app.route('/restaurants')
    def get_restaurants():
        return "This will be a list of restaurants!"

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
