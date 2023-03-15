from flask import Flask, request
from .views import blueprints
from .db import init_db

def create_app():
    app = Flask(__name__)

    init_db()

    for bp in blueprints:
        app.register_blueprint(bp)
        
    return app

